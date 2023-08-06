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

from __future__ import division, absolute_import

import logging

from traits.api import HasStrictTraits, Str, provides

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import cytoflow.utility as util
from .i_view import IView

@provides(IView)
class ViolinPlotView(HasStrictTraits):
    """Plots a violin plot -- a set of kernel density estimates
    
    Attributes
    ----------
    name : Str
        The view's name (for serialization, UI etc.)
    
    channel : Str
        the name of the channel we're plotting
        
    xvariable : Str
        the main variable by which we're faceting
    
    xfacet : Str 
        the conditioning variable for multiple plots (horizontal)
    
    yfacet : Str
        the conditioning variable for multiple plots (vertical)
    
    huefacet : Str
        the conditioning variable for multiple plots (color)
        
    subset : Str
        a string passed to pandas.DataFrame.query() to subset the data before 
        we plot it.
        
        .. note: Should this be a param instead?
        
    Examples
    --------
    >>> kde = flow.Kde1DView()
    >>> kde.name = "Kernel Density 1D"
    >>> kde.channel = 'Y2-A'
    >>> kde.xfacet = 'Dox'
    >>> kde.yfacet = 'Y2-A+'
    >>> kde.plot(ex)
    """
    
    # traits   
    id = "edu.mit.synbio.cytoflow.view.violin"
    friendly_id = "Violin Plot" 
    
    name = Str
    channel = Str
    variable = Str
    scale = util.ScaleEnum
    xfacet = Str
    yfacet = Str
    huefacet = Str
    subset = Str
    
    def plot(self, experiment, **kwargs):
        """Plot a faceted histogram view of a channel"""
        
        if not experiment:
            raise util.CytoflowViewError("No experiment specified")
        
        if not self.channel:
            raise util.CytoflowViewError("Must specify a channel")
        
        if self.channel not in experiment.data:
            raise util.CytoflowViewError("Channel {0} not in the experiment"
                                    .format(self.channel))
        
        if not self.variable:
            raise util.CytoflowViewError("Variable not specified")
        
        if not self.variable in experiment.conditions:
            raise util.CytoflowViewError("Variable {0} isn't in the experiment")
        
        if self.xfacet and self.xfacet not in experiment.conditions:
            raise util.CytoflowViewError("X facet {0} not in the experiment"
                                    .format(self.xfacet))
        
        if self.yfacet and self.yfacet not in experiment.conditions:
            raise util.CytoflowViewError("Y facet {0} not in the experiment"
                                    .format(self.yfacet))
        
        if self.huefacet and self.huefacet not in experiment.conditions:
            raise util.CytoflowViewError("Hue facet {0} not in the experiment"
                                    .format(self.huefacet))

        if self.subset:
            try:
                data = experiment.query(self.subset).data.reset_index()
            except:
                raise util.CytoflowViewError("Subset string '{0}' isn't valid"
                                        .format(self.subset))
                
            if len(data) == 0:
                raise util.CytoflowViewError("Subset string '{0}' returned no events"
                                        .format(self.subset))
        else:
            data = experiment.data
                    
        # get the scale
        scale = util.scale_factory(self.scale, experiment, self.channel)
        kwargs['data_scale'] = scale
        
        kwargs.setdefault('orient', 'v')
                
        g = sns.FacetGrid(data, 
                          size = 6,
                          aspect = 1.5,
                          col = (self.xfacet if self.xfacet else None),
                          row = (self.yfacet if self.yfacet else None),
                          col_order = (np.sort(data[self.xfacet].unique()) if self.xfacet else None),
                          row_order = (np.sort(data[self.yfacet].unique()) if self.yfacet else None),
                          legend_out = False,
                          sharex = False,
                          sharey = False)
                
        # set the scale for each set of axes; can't just call plt.xscale() 
        for ax in g.axes.flatten():
            if kwargs['orient'] == 'h':
                ax.set_xscale(self.scale, **scale.mpl_params)  
            else:
                ax.set_yscale(self.scale, **scale.mpl_params)  
            
        # this order-dependent thing weirds me out.      
        if kwargs['orient'] == 'h':
            violin_args = [self.channel, self.variable]
        else:
            violin_args = [self.variable, self.channel]
            
        if self.huefacet:
            violin_args.append(self.huefacet)
            
        g.map(_violinplot,   
              *violin_args,      
              order = np.sort(data[self.variable].unique()),
              hue_order = (np.sort(data[self.huefacet].unique()) if self.huefacet else None),
              **kwargs)
        
        # if we have an xfacet, make sure the y scale is the same for each
        fig = plt.gcf()
        fig_y_min = float("inf")
        fig_y_max = float("-inf")
        for ax in fig.get_axes():
            ax_y_min, ax_y_max = ax.get_ylim()
            if ax_y_min < fig_y_min:
                fig_y_min = ax_y_min
            if ax_y_max > fig_y_max:
                fig_y_max = ax_y_max
                
        for ax in fig.get_axes():
            ax.set_ylim(fig_y_min, fig_y_max)
            
        # if we have a yfacet, make sure the x scale is the same for each
        fig = plt.gcf()
        fig_x_min = float("inf")
        fig_x_max = float("-inf")
        
        for ax in fig.get_axes():
            ax_x_min, ax_x_max = ax.get_xlim()
            if ax_x_min < fig_x_min:
                fig_x_min = ax_x_min
            if ax_x_max > fig_x_max:
                fig_x_max = ax_x_max
        
        if self.huefacet:
            g.add_legend(title = self.huefacet)
        
# this uses an internal interface to seaborn's violin plot.

from seaborn.categorical import _ViolinPlotter

def _violinplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None,
                bw="scott", cut=2, scale="area", scale_hue=True, gridsize=100,
                width=.8, inner="box", split=False, orient=None, linewidth=None,
                color=None, palette=None, saturation=.75, ax=None, data_scale = None,
                **kwargs):
    
    if orient and orient == 'h':
        x = data_scale(x)
    else:
        y = data_scale(y)
            
    plotter = _ViolinPlotter(x, y, hue, data, order, hue_order,
                             bw, cut, scale, scale_hue, gridsize,
                             width, inner, split, orient, linewidth,
                             color, palette, saturation)

    for i in range(len(plotter.support)):
        if plotter.hue_names is None:       
            if plotter.support[i].shape[0] > 0:
                plotter.support[i] = data_scale.inverse(plotter.support[i])
        else:
            for j in range(len(plotter.support[i])):
                if plotter.support[i][j].shape[0] > 0:
                    plotter.support[i][j] = data_scale.inverse(plotter.support[i][j])

    for i in range(len(plotter.plot_data)):
        plotter.plot_data[i] = data_scale.inverse(plotter.plot_data[i])

    if ax is None:
        ax = plt.gca()

    plotter.plot(ax)
    return ax