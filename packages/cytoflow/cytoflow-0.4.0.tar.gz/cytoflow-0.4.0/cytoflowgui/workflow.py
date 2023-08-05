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

"""
The main model for the GUI.

At its core, the model is a list of WorkflowItem instances.  A WorkflowItem
wraps an operation, its completion status, the result of applying it to
the previous WorkflowItem's result, and views on that result.  The Workflow
also maintains a "current" or selected WorkflowItem.

The left panel of the GUI is a View on this object (viewing the list of
WorkflowItem instances), and the right panel of the GUI is a View of the
selected WorkflowItem's current view.

So far, so simple.  However, in a single-threaded GUI application, the UI
freezes when something processor-intensive is happening.  Adding another thread
doesn't help matters because of the CPython global interpreter lock; while
Python is otherwise computing, the GUI doesn't update.  To solve this, the 
Workflow maintains a copy of itself in a separate process.  The local Workflow
is the one that is viewed by the GUI; the remote Workflow is the one that
actually loads the data and does the processing.  Thus the GUI remains
responsive.  Changed attributes in either Workflow are noticed by a set of 
Traits handlers, which send those changes to the other process.

This process is also where the plotting happens.  For an explanation of how
the plots are ferried back to the GUI, see the module docstring for
matplotlib_backend.py
"""

import threading, sys, Queue, logging, traceback

from traits.api import HasStrictTraits, Instance, List, on_trait_change, Any
                       
from traitsui.api import View, Item, InstanceEditor, Spring, Label

import matplotlib.pyplot as plt

import cytoflow
import cytoflow.utility as util
from cytoflow.views import IView

from cytoflowgui.vertical_notebook_editor import VerticalNotebookEditor
from cytoflowgui.workflow_item import WorkflowItem, RemoteWorkflowItem
from cytoflowgui.util import UniquePriorityQueue
from cytoflowgui.multiprocess_logging import QueueHandler
import cytoflowgui.matplotlib_backend
# import cytoflowgui.util as guiutil

# pipe connections for communicating between processes
# http://stackoverflow.com/questions/1977362/how-to-create-module-wide-variables-in-python
#this = sys.modules[__name__]
#this.parent_conn = None
#this.child_conn = None

class Msg:
    NEW_WORKFLOW = "NEW_WORKFLOW"
    ADD_ITEMS = "ADD_ITEMS"
    REMOVE_ITEMS = "REMOVE_ITEMS"
    SELECT = "SELECT"
    UPDATE_OP = "UPDATE_OP"
    UPDATE_VIEW = "UPDATE_VIEW"
    CHANGE_CURRENT_VIEW = "CHANGE_CURRENT_VIEW"
    CHANGE_CURRENT_PLOT = "CHANGE_CURRENT_PLOT"
    UPDATE_WI = "UPDATE_WI"
    CHANGE_DEFAULT_SCALE = "CHANGE_DEFAULT_SCALE"
    ESTIMATE = "ESTIMATE"
    
def log_exception():
    (exc_type, exc_value, tb) = sys.exc_info()

    err_string = traceback.format_exception_only(exc_type, exc_value)[0]
    err_loc = traceback.format_tb(tb)[-1]
    err_ctx = threading.current_thread().name
    
    logging.debug("Exception in {0}: {1}"
                  .format(err_ctx,
                          "".join( traceback.format_exception(exc_type, exc_value, tb) )))
    
    logging.error("Error: {0}\nLocation: {1}Thread: {2}" \
                  .format(err_string, err_loc, err_ctx) )
    

class Workflow(HasStrictTraits):
    
    workflow = List(WorkflowItem)
    selected = Instance(WorkflowItem)

    default_scale = util.ScaleEnum
    
    # a view for the entire workflow's list of operations 
    operations_traits = View(Item('workflow',
                                  editor = VerticalNotebookEditor(view = 'operation_traits',
                                                                  page_name = '.name',
                                                                  page_description = '.friendly_id',
                                                                  page_icon = '.icon',
                                                                  delete = True,
                                                                  page_deletable = '.deletable',
                                                                  selected = 'selected',
                                                                  scrollable = True,
                                                                  multiple_open = False),
                                show_label = False))

    # a view showing the selected workflow item's current view
    selected_view_traits = View(Item('selected',
                                     editor = InstanceEditor(view = 'current_view_traits'),
                                     style = 'custom',
                                     show_label = False),
                                Spring(),
                                Label("Default scale"),
                                Item('default_scale',
                                     show_label = False))
    
    # the view for the center pane
    plot_view = View(Item('selected',
                          editor = InstanceEditor(view = 'current_plot_view'),
                          style = 'custom',
                          show_label = False))
    
    recv_thread = Instance(threading.Thread)
    send_thread = Instance(threading.Thread)
    log_thread = Instance(threading.Thread)
    remote_process_thread = Instance(threading.Thread)
    message_q = Instance(Queue.Queue, ())
    
    # the Pipe connection object to pass to the matplotlib canvas
    child_matplotlib_conn = Any
    
    def __init__(self, remote_connection, **kwargs):
        super(Workflow, self).__init__(**kwargs)  
        
        child_workflow_conn, self.child_matplotlib_conn, log_q = remote_connection
        
        self.recv_thread = threading.Thread(target = self.recv_main, 
                                            name = "local workflow recv",
                                            args = [child_workflow_conn])
        self.recv_thread.daemon = True
        self.recv_thread.start()
        
        self.send_thread = threading.Thread(target = self.send_main,
                                            name = "local workflow send",
                                            args = [child_workflow_conn])
        self.send_thread.daemon = True
        self.send_thread.start()
        
        self.log_thread = threading.Thread(target = self.log_main,
                                           name = "log listener thread",
                                           args = [log_q])
        self.log_thread.daemon = True
        self.log_thread.start()
        

    def recv_main(self, child_conn):
        while child_conn.poll(None):
            try:
                (msg, payload) = child_conn.recv()
            except EOFError:
                return
            
            logging.debug("LocalWorkflow.recv_main :: {}".format(msg))
            
        
            try: 
                if msg == Msg.UPDATE_WI:
                    (idx, new_wi) = payload
                    wi = self.workflow[idx]
                    wi.copy_traits(new_wi, status = True)
                        
                elif msg == Msg.UPDATE_OP:
                    (idx, new_op, update_type) = payload
                    wi = self.workflow[idx]
                    wi.operation.copy_traits(new_op, 
                                             status = True,
                                             fixed = lambda t: t is not True)
                    
                    wi.operation.changed = update_type
                    
                elif msg == Msg.UPDATE_VIEW:
                    (idx, new_view, update_type) = payload
                    view_id = new_view.id
                    wi = self.workflow[idx]
                    view = next((x for x in wi.views if x.id == view_id))
                    view.copy_traits(new_view, 
                                     status = True,
                                     fixed = lambda t: t is not True)
                    
                    view.changed = update_type
                else:
                    raise RuntimeError("Bad message from remote")
            
            except Exception:
                log_exception()

    
    def send_main(self, child_conn):
        while True:
            msg = self.message_q.get()
            child_conn.send(msg)

            
    def log_main(self, log_q):
        # from http://plumberjack.blogspot.com/2010/09/using-logging-with-multiprocessing.html
        
        while True:
            try:
                record = log_q.get()
                if record is None: # We send this as a sentinel to tell the listener to quit.
                    break
                logger = logging.getLogger(record.name)
                logger.handle(record) # No level or filter logic applied - just do it!
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                print >> sys.stderr, 'Whoops! Problem:'
                traceback.print_exc(file=sys.stderr)

    @on_trait_change('workflow')
    def _on_new_workflow(self, obj, name, old, new):
        logging.debug("LocalWorkflow._on_new_workflow")
            
        self.selected = None
        
        # send the new workflow to the child process
        self.message_q.put((Msg.NEW_WORKFLOW, self.workflow))
        
        
    @on_trait_change('workflow_items')
    def _on_workflow_add_remove_items(self, event):
        logging.debug("LocalWorkflow._on_workflow_add_remove_items :: {}"
                      .format((event.index, event.removed, event.added)))

        idx = event.index
        
        # remove deleted items from the linked list
        if event.removed:
            assert len(event.removed) == 1
            removed = event.removed[0]
            if removed.previous:
                removed.previous.next = removed.next
                
            if removed.next:
                removed.next.previous = removed.previous
            
            self.message_q.put((Msg.REMOVE_ITEMS, idx))
            
            if removed == self.selected:
                self.selected = None

        
        # add new items to the linked list
        if event.added:
            assert len(event.added) == 1
            if idx > 0:
                self.workflow[idx - 1].next = self.workflow[idx]
                self.workflow[idx].previous = self.workflow[idx - 1]
                
            if idx < len(self.workflow) - 1:
                self.workflow[idx].next = self.workflow[idx + 1]
                self.workflow[idx + 1].previous = self.workflow[idx]
                
            self.message_q.put((Msg.ADD_ITEMS, (idx, event.added[0])))
 
    @on_trait_change('selected')
    def _on_selected_changed(self, obj, name, old, new):
        logging.debug("LocalWorkflow._on_selected_changed :: {}"
                      .format((obj, name, old, new)))
            
        if new is None:
            idx = -1
        else:
            idx = self.workflow.index(new)
            
        self.message_q.put((Msg.SELECT, idx))
        
    @on_trait_change('workflow:operation:changed')
    def _operation_changed(self, obj, name, new):
        logging.debug("LocalWorkflow._operation_changed :: {}"
                      .format(obj, new))
        
        if new == "api" or new == "estimate":         
            wi = next((x for x in self.workflow if x.operation == obj))
            idx = self.workflow.index(wi)
            self.message_q.put((Msg.UPDATE_OP, (idx, obj, new)))

    @on_trait_change('workflow:views:changed')
    def _view_changed(self, obj, name, new):
        logging.debug("LocalWorkflow._view_changed :: {}"
                      .format((obj, name, new)))

        if new == "api":
            wi = next((x for x in self.workflow if obj in x.views))
            idx = self.workflow.index(wi)
            self.message_q.put((Msg.UPDATE_VIEW, (idx, obj, new)))
        
    @on_trait_change('workflow:current_view')
    def _on_current_view_changed(self, obj, name, old, new):
        logging.debug("LocalWorkflow._on_current_view_changed :: {}"
                      .format((obj, name, old, new)))                  
                  
        idx = self.workflow.index(obj)
        view = obj.current_view
        self.message_q.put((Msg.CHANGE_CURRENT_VIEW, (idx, view)))

    @on_trait_change('workflow:current_plot')
    def _on_current_plot_changed(self, obj, name, old, new):
        logging.debug("LocalWorkflow._on_current_plot_changed :: {}"
                      .format((obj, name, old, new)))                  
                  
        idx = self.workflow.index(obj)
        plot = obj.current_plot
        self.message_q.put((Msg.CHANGE_CURRENT_PLOT, (idx, plot)))
        
    @on_trait_change('workflow:do_estimate')
    def _on_estimate(self, obj, name, old, new):
        logging.debug("LocalWorkflow._on_estimate :: {}"
                      .format((obj, name, old, new)))
        idx = self.workflow.index(obj)
        self.message_q.put((Msg.ESTIMATE, idx))

    # MAGIC: called when default_scale is changed
    def _default_scale_changed(self, new_scale):
        logging.debug("LocalWorkflow._default_scale_changed :: {}"
                      .format((new_scale)))
            
        cytoflow.set_default_scale(new_scale)
        self.message_q.put((Msg.CHANGE_DEFAULT_SCALE, new_scale))

        
class RemoteWorkflow(HasStrictTraits):
    workflow = List(RemoteWorkflowItem)
    selected = Instance(RemoteWorkflowItem)
    
    plot_lock = Instance(threading.Lock, ())
    last_view_plotted = Instance(IView)
    
    send_thread = Instance(threading.Thread)
    recv_thread = Instance(threading.Thread)
    message_q = Instance(Queue.Queue, ())
    
    # synchronization primitives for plotting
    matplotlib_events = Any
    plot_lock = Any
    
    exec_q = Instance(UniquePriorityQueue, ())
    
    def run(self, parent_workflow_conn, parent_mpl_conn, log_q):
        
        # if we're on MacOS or Linux, we inherit a root logger config from the 
        # parent process.  clear it.
        
        rootLogger = logging.getLogger()
        map(rootLogger.removeHandler, rootLogger.handlers[:])
        map(rootLogger.removeFilter, rootLogger.filters[:])
        
        # make queue messages go to log_q
        h = QueueHandler(log_q) 
        rootLogger.addHandler(h)
        rootLogger.setLevel(logging.DEBUG)
        
        # set up the plotting synchronization primitives
        self.matplotlib_events = threading.Event()
        self.plot_lock = threading.Lock()
        
        # configure matplotlib backend to use the pipe
        plt.new_figure_manager = lambda num, parent_conn = parent_mpl_conn, process_events = self.matplotlib_events, *args, **kwargs: \
                                    cytoflowgui.matplotlib_backend.new_figure_manager(num, 
                                                                                      parent_conn = parent_conn, 
                                                                                      process_events = process_events, 
                                                                                      *args, 
                                                                                      **kwargs)
        
        # start threads
        self.recv_thread = threading.Thread(target = self.recv_main, 
                             name = "remote recv thread",
                             args = [parent_workflow_conn])
        self.recv_thread.daemon = True
        self.recv_thread.start()
        
        self.send_thread = threading.Thread(target = self.send_main,
                                            name = "remote send thread",
                                            args = [parent_workflow_conn])
        self.send_thread.daemon = True
        self.send_thread.start()
        
        # loop and process updates
        while True:
            try:
                _, fn = self.exec_q.get()
                fn()
            except Exception:
                log_exception()
            

    def recv_main(self, parent_conn):
        while parent_conn.poll(None):
            try:
                (msg, payload) = parent_conn.recv()
            except EOFError:
                return
            
            logging.debug("RemoteWorkflow.recv_main :: {}".format(msg))
            
            try:
                if msg == Msg.NEW_WORKFLOW:
                    self.workflow = []
                    for new_item in payload:
                        wi = RemoteWorkflowItem()
                        wi.copy_traits(new_item)
                        wi.matplotlib_events = self.matplotlib_events
                        wi.plot_lock = self.plot_lock
                        self.workflow.append(wi)
                    self.workflow[0].command = "apply"
    
                elif msg == Msg.ADD_ITEMS:
                    (idx, new_item) = payload
                    wi = RemoteWorkflowItem()
                    wi.copy_traits(new_item)
                    wi.matplotlib_events = self.matplotlib_events
                    wi.plot_lock = self.plot_lock
                    
                    self.workflow.insert(idx, wi)
    
                elif msg == Msg.REMOVE_ITEMS:
                    idx = payload
                    self.workflow.remove(self.workflow[idx])
                    
                elif msg == Msg.SELECT:
                    idx = payload
                    if idx == -1:
                        self.selected = None
                    else:
                        self.selected = self.workflow[idx]
                    
                elif msg == Msg.UPDATE_OP:
                    (idx, new_op, update_type) = payload
                    wi = self.workflow[idx]
                    wi.operation.copy_traits(new_op, 
                                             status = lambda t: t is not True,
                                             fixed = lambda t: t is not True)
                    
                    wi.operation.changed = update_type
                        
                elif msg == Msg.UPDATE_VIEW:
                    (idx, new_view, update_type) = payload
                    view_id = new_view.id
                    wi = self.workflow[idx]
                    try:
                        view = next((x for x in wi.views if x.id == view_id))
                    except StopIteration:
                        logging.warn("RemoteWorkflow: Couldn't find view {}".format(view_id))
                        continue
                    
                    view.copy_traits(new_view, 
                                     status = lambda t: t is not True,
                                     fixed = lambda t: t is not True) 
                    
                    view.changed = update_type
    
                elif msg == Msg.CHANGE_CURRENT_VIEW:
                    (idx, view) = payload
                    wi = self.workflow[idx]
                    try:
                        wi.current_view = next((x for x in wi.views if x.id == view.id))
                    except StopIteration:
                        wi.views.append(view)
                        wi.current_view = view
                        
                    wi.command = "plot"
                        
                elif msg == Msg.CHANGE_CURRENT_PLOT:
                    (idx, plot) = payload
                    wi = self.workflow[idx]
                    wi.current_plot = plot
                    
                    #wi.command = "plot"
                    
                    #self.exec_q.put_nowait((0, wi.plot))
                        
                elif msg == Msg.CHANGE_DEFAULT_SCALE:
                    new_scale = payload
                    cytoflow.set_default_scale(new_scale)
                    
                elif msg == Msg.ESTIMATE:
                    idx = payload
                    wi = self.workflow[idx]
                    
                    wi.command = "estimate"
                    #self.exec_q.put_nowait((idx - 0.1, wi.estimate))
    
                else:
                    raise RuntimeError("Bad command in the remote workflow")
            
            except Exception:
                log_exception()
            
    def send_main(self, parent_conn):
        while True:
            msg = self.message_q.get()
            parent_conn.send(msg)
            
            
    @on_trait_change('workflow_items')
    def _on_workflow_add_remove_items(self, event):
        logging.debug("RemoteWorkflow._on_workflow_add_remove_items :: {}"
                      .format((event.index, event.removed, event.added)))
            
        idx = event.index

        # remove deleted items from the linked list
        if event.removed:
            assert len(event.removed) == 1
            removed = event.removed[0]
            if removed.previous:
                removed.previous.next = removed.next
                
            if removed.next:
                removed.next.previous = removed.previous
        
        # add new items to the linked list
        if event.added:
            assert len(event.added) == 1
            if idx > 0:
                self.workflow[idx - 1].next = self.workflow[idx]
                self.workflow[idx].previous = self.workflow[idx - 1]
                
            if idx < len(self.workflow) - 1:
                self.workflow[idx].next = self.workflow[idx + 1]
                self.workflow[idx + 1].previous = self.workflow[idx]
                
                
    @on_trait_change('workflow:views:changed')
    def _view_trait_changed(self, obj, name, new):
        logging.debug("RemoteWorkflow._view_changed :: {}"
                      .format((obj, name, new)))

        wi = next((x for x in self.workflow if obj in x.views))
        idx = self.workflow.index(wi)
        
        if new == "status":
            self.message_q.put((Msg.UPDATE_VIEW, (idx, obj, new)))
            
            
    @on_trait_change('workflow:operation:changed')
    def _operation_changed(self, obj, name, new):
        logging.debug("RemoteWorkflow._operation_changed :: {}"
                      .format(obj))
        
        wi = next((x for x in self.workflow if x.operation == obj))
        idx = self.workflow.index(wi)      
            
        if new == "status":
            self.message_q.put((Msg.UPDATE_OP, (idx, obj, new)))
            

    @on_trait_change('workflow:changed')
    def _workflow_item_changed(self, obj, name, old, new):
        logging.debug("RemoteWorkflow._workflow_status_changed :: {}"
                      .format((obj, name, old, new)))
            
        idx = self.workflow.index(obj)            
        self.message_q.put((Msg.UPDATE_WI, (idx, obj)))
            
    @on_trait_change('workflow:command')
    def _workflow_command(self, obj, name, cmd):
        logging.debug("RemoteWorkflow._workflow_command :: {}"
                      .format((obj, name, cmd)))
        
        idx = self.workflow.index(obj)            

        if cmd == "apply":
            self.exec_q.put_nowait((idx, obj.apply))
        elif cmd == "estimate":
            self.exec_q.put_nowait((idx - 0.1, obj.estimate))
        elif cmd == "plot" and obj == self.selected:
            self.exec_q.put_nowait((0, obj.plot))
            
    @on_trait_change('selected')
    def _selected_changed(self, obj, name, new):
        if new:
            new.command = "plot"
        