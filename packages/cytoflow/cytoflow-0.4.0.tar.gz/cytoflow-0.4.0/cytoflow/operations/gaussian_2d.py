#!/usr/bin/env python2.7

# (c) Massachusetts Institute of Technology 2015-2016
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Created on Dec 16, 2015

@author: brian
'''

from __future__ import division, absolute_import

import warnings, random, string

from traits.api import (HasStrictTraits, Str, CStr, Dict, Any, Instance, Bool, 
                        Constant, List, provides, DelegatesTo)

import numpy as np
import matplotlib.pyplot as plt
from sklearn import mixture
from scipy import linalg
import pandas as pd
import seaborn as sns

import cytoflow.views
import cytoflow.utility as util

from .i_operation import IOperation

@provides(IOperation)
class GaussianMixture2DOp(HasStrictTraits):
    """
    This module fits a 2D Gaussian mixture model with a specified number of
    components to a pair of channels.
    
    Creates a new categorical metadata variable named `name`, with possible
    values `name_1` .... `name_n` where `n` is the number of components.
    An event is assigned to `name_i` category if it falls within `sigma`
    standard deviations of the component's mean.  If that is true for multiple
    categories (or if `sigma == 0.0`), the event is assigned to the category 
    with the highest posterior probability.  If the event doesn't fall into
    any category, it is assigned to `name_None`.
    
    As a special case, if `num_components` is `1` and `sigma` > 0.0, then
    the new condition is boolean, `True` if the event fell in the gate and
    `False` otherwise.
    
    Optionally, if `posteriors` is `True`, this module will also compute the 
    posterior probability of each event in its assigned component, returning
    it in a new colunm named `{Name}_Posterior`.
    
    Finally, the same mixture model (mean and standard deviation) may not
    be appropriate for every subset of the data.  If this is the case, you
    can use the `by` attribute to specify metadata by which to aggregate
    the data before estimating (and applying) a mixture model.  The number of 
    components is the same across each subset, though.
    
    Attributes
    ----------
    name : Str
        The operation name; determines the name of the new metadata column
        
    xchannel : Str
        The X channel to apply the mixture model to.
        
    ychannel : Str
        The Y channel to apply the mixture model to.

    xscale : Enum("linear", "logicle", "log") (default = "linear")
        Re-scale the data on the X acis before fitting the data?  

    yscale : Enum("linear", "logicle", "log") (default = "linear")
        Re-scale the data on the Y axis before fitting the data?  
        
    num_components : Int (default = 1)
        How many components to fit to the data?  Must be positive.

    sigma : Float (default = 0.0)
        How many standard deviations on either side of the mean to include
        in each category?  If an event is in multiple components, assign it
        to the component with the highest posterior probability.  If 
        `sigma == 0.0`, categorize *all* the data by assigning each event to
        the component with the highest posterior probability.  Must be >= 0.0.
    
    by : List(Str)
        A list of metadata attributes to aggregate the data before estimating
        the model.  For example, if the experiment has two pieces of metadata,
        `Time` and `Dox`, setting `by = ["Time", "Dox"]` will fit the model 
        separately to each subset of the data with a unique combination of
        `Time` and `Dox`.

    posteriors : Bool (default = False)
        If `True`, add a column named `{Name}_Posterior` giving the posterior
        probability that the event is in the component to which it was
        assigned.  Useful for filtering out low-probability events.
    
    Examples
    --------
    
    >>> gauss_op = GaussianMixture2DOp(name = "Gaussian",
    ...                                xchannel = "V2-A",
    ...                                ychannel = "Y2-A",
    ...                                num_components = 2)
    >>> gauss_op.estimate(ex2)
    >>> gauss_op.default_view().plot(ex2)
    >>> ex3 = gauss_op.apply(ex2)
    """
    
    id = Constant('edu.mit.synbio.cytoflow.operations.gaussian_2d')
    friendly_id = Constant("2D Gaussian Mixture")
    
    name = CStr()
    xchannel = Str()
    ychannel = Str()
    xscale = util.ScaleEnum
    yscale = util.ScaleEnum
    num_components = util.PositiveInt
    sigma = util.PositiveFloat(0.0, allow_zero = True)
    by = List(Str)
    
    posteriors = Bool(False)
    
    # the key is either a single value or a tuple
    _gmms = Dict(Any, Instance(mixture.GMM), transient = True)
    _xscale = Instance(util.IScale, transient = True)
    _yscale = Instance(util.IScale, transient = True)
    
    def estimate(self, experiment, subset = None):
        """
        Estimate the Gaussian mixture model parameters
        """
        
        if not experiment:
            raise util.CytoflowOpError("No experiment specified")

        if self.xchannel not in experiment.data:
            raise util.CytoflowOpError("Column {0} not found in the experiment"
                                  .format(self.xchannel))
            
        if self.ychannel not in experiment.data:
            raise util.CytoflowOpError("Column {0} not found in the experiment"
                                  .format(self.ychannel))
       
        for b in self.by:
            if b not in experiment.data:
                raise util.CytoflowOpError("Aggregation metadata {0} not found"
                                      " in the experiment"
                                      .format(b))
            if len(experiment.data[b].unique()) > 100: #WARNING - magic number
                raise util.CytoflowOpError("More than 100 unique values found for"
                                      " aggregation metadata {0}.  Did you"
                                      " accidentally specify a data channel?"
                                      .format(b))
                
        if subset:
            try:
                experiment = experiment.query(subset)
            except:
                raise util.CytoflowViewError("Subset string '{0}' isn't valid"
                                        .format(subset))
                
            if len(experiment) == 0:
                raise util.CytoflowViewError("Subset string '{0}' returned no events"
                                        .format(subset))
                
        if self.by:
            groupby = experiment.data.groupby(self.by)
        else:
            # use a lambda expression to return a group that contains
            # all the events
            groupby = experiment.data.groupby(lambda x: True)
            
        # get the scale. estimate the scale params for the ENTIRE data set,
        # not subsets we get from groupby().  And we need to save it so that
        # the data is transformed the same way when we apply()
        self._xscale = util.scale_factory(self.xscale, experiment, self.xchannel)
        self._yscale = util.scale_factory(self.yscale, experiment, self.ychannel)
        
        gmms = {}
            
        for group, data_subset in groupby:
            if len(data_subset) == 0:
                raise util.CytoflowOpError("Group {} had no data"
                                           .format(group))
            x = data_subset.loc[:, [self.xchannel, self.ychannel]]
            x[self.xchannel] = self._xscale(x[self.xchannel])
            x[self.ychannel] = self._yscale(x[self.ychannel])
            
            # drop data that isn't in the scale range
            x = x[~(np.isnan(x[self.xchannel]) | np.isnan(x[self.ychannel]))]
            x = x.values
            
            gmm = mixture.GMM(n_components = self.num_components,
                              covariance_type = "full",
                              random_state = 1)
            gmm.fit(x)
            
            if not gmm.converged_:
                raise util.CytoflowOpError("Estimator didn't converge"
                                      " for group {0}"
                                      .format(group))
                
            # in the 1D version, we sort the components by the means -- so
            # the first component has the lowest mean, the second component
            # has the next-lowest mean, etc.  that doesn't work in a 2D area,
            # obviously.
            
            # instead, we assume that the clusters are likely (?) to be
            # arranged along *one* of the axes, so we take the |norm| of the
            # x,y mean of each cluster and sort that way.
            
            norms = (gmm.means_[:, 0] ** 2 + gmm.means_[:, 1] ** 2) ** 0.5
            sort_idx = np.argsort(norms)
            gmm.means_ = gmm.means_[sort_idx]
            gmm.weights_ = gmm.weights_[sort_idx]
            gmm.covars_ = gmm.covars_[sort_idx]
            
            gmms[group] = gmm
            
        self._gmms = gmms
    
    def apply(self, experiment):
        """
        Assigns new metadata to events using the mixture model estimated
        in `estimate`.
        """
            
        if not experiment:
            raise util.CytoflowOpError("No experiment specified")
        
        if not self.xchannel:
            raise util.CytoflowOpError("Must set X channel")

        if not self.ychannel:
            raise util.CytoflowOpError("Must set Y channel")
        
        # make sure name got set!
        if not self.name:
            raise util.CytoflowOpError("You have to set the gate's name "
                                  "before applying it!")

        if self.name in experiment.data.columns:
            raise util.CytoflowOpError("Experiment already has a column named {0}"
                                  .format(self.name))
        
        if not self._gmms:
            raise util.CytoflowOpError("No components found.  Did you forget to "
                                  "call estimate()?")
            
        if not self._xscale:
            raise util.CytoflowOpError("Couldn't find _xscale.  What happened??")
        
        if not self._yscale:
            raise util.CytoflowOpError("Couldn't find _yscale.  What happened??")

        if self.xchannel not in experiment.data:
            raise util.CytoflowOpError("Column {0} not found in the experiment"
                                  .format(self.xchannel))

        if self.ychannel not in experiment.data:
            raise util.CytoflowOpError("Column {0} not found in the experiment"
                                  .format(self.ychannel))
            
        if (self.name + "_Posterior") in experiment.data:
            raise util.CytoflowOpError("Column {0} already found in the experiment"
                                  .format(self.name + "_Posterior"))
            
        if self.num_components == 1 and self.sigma == 0.0:
            raise util.CytoflowOpError("If num_components == 1, sigma must be > 0")

        if self.posteriors:
            col_name = "{0}_Posterior".format(self.name)
            if col_name in experiment.data:
                raise util.CytoflowOpError("Column {0} already found in the experiment"
                              .format(col_name))
       
        for b in self.by:
            if b not in experiment.data:
                raise util.CytoflowOpError("Aggregation metadata {0} not found"
                                      " in the experiment"
                                      .format(b))

            if len(experiment.data[b].unique()) > 100: #WARNING - magic number
                raise util.CytoflowOpError("More than 100 unique values found for"
                                      " aggregation metadata {0}.  Did you"
                                      " accidentally specify a data channel?"
                                      .format(b))
                           
        if self.sigma < 0.0:
            raise util.CytoflowOpError("sigma must be >= 0.0")
        
        event_assignments = pd.Series([None] * len(experiment), dtype = "object")

        if self.posteriors:
            event_posteriors = pd.Series([0.0] * len(experiment))
            
        # what we DON'T want to do is iterate through event-by-event.
        # the more of this we can push into numpy, sklearn and pandas,
        # the faster it's going to be.  for example, this is why
        # we don't use Ellipse.contains().  
        
        if self.by:
            groupby = experiment.data.groupby(self.by)
        else:
            # use a lambda expression to return a group that
            # contains all the events
            groupby = experiment.data.groupby(lambda x: True)
        
        for group, data_subset in groupby:
            if group not in self._gmms:
                # there weren't any events in this group, so we didn't get
                # a gmm.
                continue
            
            gmm = self._gmms[group]
            x = data_subset.loc[:, [self.xchannel, self.ychannel]]
            x[self.xchannel] = self._xscale(x[self.xchannel])
            x[self.ychannel] = self._yscale(x[self.ychannel])
            
            # which values are missing?
            x_na = np.isnan(x[self.xchannel]) | np.isnan(x[self.ychannel])
            x_na = x_na.values
            
            x = x.values
            group_idx = groupby.groups[group]

            # make a preliminary assignment
            predicted = np.full(len(x), -1, "int")
            predicted[~x_na] = gmm.predict(x[~x_na])
            
            # if we're doing sigma-based gating, for each component check
            # to see if the event is in the sigma gate.
            if self.sigma > 0.0:
                
                # make a quick dataframe with the value and the predicted
                # component
                gate_df = pd.DataFrame({"x" : x[:, 0], 
                                        "y" : x[:, 1],
                                        "p" : predicted})

                # for each component, get the ellipse that follows the isoline
                # around the mixture component
                # cf. http://scikit-learn.org/stable/auto_examples/mixture/plot_gmm.html
                # and http://www.mathworks.com/matlabcentral/newsreader/view_thread/298389
                # and http://stackoverflow.com/questions/7946187/point-and-ellipse-rotated-position-test-algorithm
                # i am not proud of how many tries this took me to get right.

                for c in range(0, self.num_components):
                    mean = gmm.means_[c]
                    covar = gmm._get_covars()[c]
                    
                    # xc is the center on the x axis
                    # yc is the center on the y axis
                    xc = mean[0]  # @UnusedVariable
                    yc = mean[1]  # @UnusedVariable
                    
                    v, w = linalg.eigh(covar)
                    u = w[0] / linalg.norm(w[0])
                    
                    # xl is the length along the x axis
                    # yl is the length along the y axis
                    xl = np.sqrt(v[0]) * self.sigma  # @UnusedVariable
                    yl = np.sqrt(v[1]) * self.sigma  # @UnusedVariable
                    
                    # t is the rotation in radians (counter-clockwise)
                    t = 2 * np.pi - np.arctan(u[1] / u[0])
                    
                    sin_t = np.sin(t)  # @UnusedVariable
                    cos_t = np.cos(t)  # @UnusedVariable
                                        
                    # and build an expression with numexpr so it evaluates fast!

                    gate_bool = gate_df.eval("p == @c and "
                                             "((x - @xc) * @cos_t - (y - @yc) * @sin_t) ** 2 / ((@xl / 2) ** 2) + "
                                             "((x - @xc) * @sin_t + (y - @yc) * @cos_t) ** 2 / ((@yl / 2) ** 2) <= 1").values

                    predicted[np.logical_and(predicted == c, gate_bool == False)] = -1
            
            predicted_str = pd.Series(["(none)"] * len(predicted))
            for c in range(0, self.num_components):
                predicted_str[predicted == c] = "{0}_{1}".format(self.name, c + 1)
            predicted_str[predicted == -1] = "{0}_None".format(self.name)
            predicted_str.index = group_idx

            event_assignments.iloc[group_idx] = predicted_str
                    
            if self.posteriors:
                probability = np.full((len(x), self.num_components), 0.0, "float")
                probability[~x_na, :] = gmm.predict_proba(x[~x_na, :])
                posteriors = pd.Series([0.0] * len(predicted))
                for c in range(0, self.num_components):
                    posteriors[predicted == c] = probability[predicted == c, c]
                posteriors.index = group_idx
                event_posteriors.iloc[group_idx] = posteriors
                    
        new_experiment = experiment.clone()
        
        if self.num_components == 1:
            new_experiment.add_condition(self.name, "bool", event_assignments == "{0}_1".format(self.name))
        else:
            new_experiment.add_condition(self.name, "category", event_assignments)
            
        if self.posteriors:
            col_name = "{0}_Posterior".format(self.name)
            new_experiment.add_condition(col_name, "float", event_posteriors)
                    
        new_experiment.history.append(self.clone_traits(transient = lambda t: True))
        return new_experiment
    
    def default_view(self, **kwargs):
        """
        Returns a diagnostic plot of the Gaussian mixture model.
        
        Returns
        -------
            IView : an IView, call plot() to see the diagnostic plot.
        """
        return GaussianMixture2DView(op = self, **kwargs)
    
    
# a few more imports for drawing scaled ellipses
        
import matplotlib.path as path
import matplotlib.patches as patches
import matplotlib.transforms as transforms
    
@provides(cytoflow.views.IView)
class GaussianMixture2DView(HasStrictTraits):
    """
    Attributes
    ----------
    name : Str
        The instance name (for serialization, UI etc.)
        
    op : Instance(GaussianMixture2DOp)
        The op whose parameters we're viewing.
        
    group : Python (default: None)
        The subset of data to display.  Must match one of the keys of 
        `op._gmms`.  If `None` (the default), display a plot for each subset.
    """
    
    id = 'edu.mit.synbio.cytoflow.view.gaussianmixture2dview'
    friendly_id = "2D Gaussian Mixture Diagnostic Plot"
    
    # TODO - why can't I use GaussianMixture2DOp here?
    op = Instance(IOperation)
    name = DelegatesTo('op')
    xchannel = DelegatesTo('op')
    ychannel = DelegatesTo('op')
    xscale = DelegatesTo('op')
    yscale = DelegatesTo('op')
    subset = Str
    
    def enum_plots(self, experiment):
        """
        Returns an iterator over the possible plots that this View can
        produce.  The values returned can be passed to "plot".
        """
        
        class plot_enum(object):
            
            def __init__(self, op, experiment):
                self._iter = None
                self._returned = False
                if op.by:
                    self._iter = experiment.data.groupby(op.by).__iter__()
                
            def __iter__(self):
                return self
            
            def next(self):
                if self._iter:
                    return self._iter.next()[0]
                else:
                    if self._returned:
                        raise StopIteration
                    else:
                        self._returned = True
                        return None
            
        return plot_enum(self.op, experiment)
    
    def plot(self, experiment, plot_name = None, **kwargs):
        """
        Plot the plots.
        """
        
        if not experiment:
            raise util.CytoflowViewError("No experiment specified")
        
        if not self.xchannel:
            raise util.CytoflowViewError("No X channel specified")
                   
        if self.xchannel not in experiment.data:
            raise util.CytoflowViewError("X channel {0} not found in the experiment"
                                  .format(self.channel))

        if not self.ychannel:
            raise util.CytoflowViewError("No Y channel specified")
                   
        if self.ychannel not in experiment.data:
            raise util.CytoflowViewError("Y channel {0} not found in the experiment"
                                  .format(self.channel))
        
        if self.op.by and not plot_name:
            for plot in self.enum_plots(experiment):
                self.plot(experiment, plot, **kwargs)
                plt.title("{0} = {1}".format(self.op.by, plot))
            return
        
        temp_experiment = experiment.clone()
        
        if plot_name:
            if plot_name and not self.op.by:
                raise util.CytoflowViewError("Plot {} not from plot_enum"
                                             .format(plot_name))
                
            groupby = experiment.data.groupby(self.op.by)
            
            if plot_name not in set(groupby.groups.keys()):
                raise util.CytoflowViewError("Plot {} not from plot_enum"
                                             .format(plot_name))
            
            temp_experiment.data = groupby.get_group(plot_name)
            temp_experiment.data.reset_index(drop = True, inplace = True)
            
        try:
            temp_op = GaussianMixture2DOp()
            temp_op.copy_traits(self.op, transient = lambda x: True)
            if not self.name:
                warnings.warn("Operation name not set!", util.CytoflowViewWarning)
                temp_op.name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
                kwargs.setdefault("legend", False)
            temp_experiment = temp_op.apply(temp_experiment)
            cytoflow.ScatterplotView(xchannel = self.xchannel,
                                     ychannel = self.ychannel,
                                     xscale = self.xscale,
                                     yscale = self.yscale,
                                     huefacet = temp_op.name,
                                     subset = self.subset).plot(temp_experiment, **kwargs)
            if plot_name:
                plt.title("{0} = {1}".format(self.op.by, plot_name))

        except util.CytoflowOpError as e:
            warnings.warn(e.__str__(), util.CytoflowViewWarning)
            cytoflow.ScatterplotView(xchannel = self.xchannel,
                                     ychannel = self.ychannel,
                                     xscale = self.xscale,
                                     yscale = self.yscale,
                                     subset = self.subset).plot(temp_experiment, **kwargs)
            if plot_name:
                plt.title("{0} = {1}".format(self.op.by, plot_name))
                
            return

        
        # plot the actual distribution on top of it.  display as a "contour"
        # plot with ellipses at 1, 2, and 3 standard deviations
        # cf. http://scikit-learn.org/stable/auto_examples/mixture/plot_gmm.html
        
        if plot_name:
            if plot_name in self.op._gmms:
                gmm = self.op._gmms[plot_name]
            else:
                # there weren't any events in this subset to estimate a GMM from
                warnings.warn("No estimated GMM for plot {}".format(plot_name),
                              util.CytoflowViewWarning)
                return
        else:
            gmm = self.op._gmms[True] 
        
        for i, (mean, covar) in enumerate(zip(gmm.means_, gmm._get_covars())):    
            v, w = linalg.eigh(covar)
            u = w[0] / linalg.norm(w[0])
            
            #rotation angle (in degrees)
            t = np.arctan(u[1] / u[0])
            t = 180 * t / np.pi
                       
            color_i = i % len(sns.color_palette())
            color = sns.color_palette()[color_i]
            
            # in order to scale the ellipses correctly, we have to make them
            # ourselves out of an affine-scaled unit circle.  The interface
            # is the same as matplotlib.patches.Ellipse
            
            self._plot_ellipse(mean,
                               np.sqrt(v[0]),
                               np.sqrt(v[1]),
                               180 + t,
                               color = color,
                               fill = False,
                               linewidth = 2)

            self._plot_ellipse(mean,
                               np.sqrt(v[0]) * 2,
                               np.sqrt(v[1]) * 2,
                               180 + t,
                               color = color,
                               fill = False,
                               linewidth = 2,
                               alpha = 0.66)
            
            self._plot_ellipse(mean,
                               np.sqrt(v[0]) * 3,
                               np.sqrt(v[1]) * 3,
                               180 + t,
                               color = color,
                               fill = False,
                               linewidth = 2,
                               alpha = 0.33)
                         
    def _plot_ellipse(self, center, width, height, angle, **kwargs):
        tf = transforms.Affine2D() \
             .scale(width * 0.5, height * 0.5) \
             .rotate_deg(angle) \
             .translate(*center)
             
        tf_path = tf.transform_path(path.Path.unit_circle())
        v = tf_path.vertices
        v = np.vstack((self.op._xscale.inverse(v[:, 0]),
                       self.op._yscale.inverse(v[:, 1]))).T

        scaled_path = path.Path(v, tf_path.codes)
        scaled_patch = patches.PathPatch(scaled_path, **kwargs)
        plt.gca().add_patch(scaled_patch)
            
             

    
