"""
File: helpers.py
Author: Gabe Venegas
Purpose: Helpers for the live matplotlib graphs
"""

import matplotlib.pyplot as plt

class Line:
    """Line object to encapsulate iterative appending"""
    def __init__(self, name, ax: plt.Axes):
        self.x = []
        self.y = []
        self.line2d = ax.plot(self.x, self.y, label=name)[0]
            
    def append(self, x, y):
        """Append a data point to plot line"""
        self.x.append(x)
        self.y.append(y)
        self.line2d.set_data(self.x, self.y)
        
    def __del__(self):
        self.line2d.remove()
        
class LinesHandler:
    """Structure to manage collection of Line objects."""
    def __init__(self, ax: plt.Axes, fig: plt.Figure, enable_pick_event: bool):
        self.ax = ax
        self.lines: dict[str, Line] = {}
        self.legendhandler = LegendHandler(ax, fig, enable_pick_event)
        
    def get_lines(self):
        """Return lines as list[plt.Line2D]"""
        return [ln.line2d for ln in self.lines.values()]
    
    def append(self, name, x, y):
        """Append data to line named 'name'."""
        if name not in self.lines:
            self.lines[name] = Line(name, self.ax)
            self.legendhandler.refresh_map(self.get_lines())
        self.lines[name].append(x, y)
        
    def clear_all(self):
        """Delete lines, clearing them from graph"""
        self.lines.clear()
        self.legendhandler.clear()

class LegendHandler:
    """Handles legend updates and toggle line visibility."""
    def __init__(self, ax: plt.Axes, fig: plt.Figure, enable_pick_event: bool):
        self.ax = ax
        self.lines: dict[plt.Line2D, plt.Line2D]= {}  # legend line to ax line
        if enable_pick_event:
            fig.canvas.mpl_connect('pick_event', self.on_pick)
    
    def on_pick(self, event):
        """Toggle visibility of plot line on legend click."""
        if not isinstance(event.artist, plt.Line2D):
            return
        if event.artist not in self.lines:
            return
        lgl = event.artist
        axl = self.lines[lgl]
        vis = not axl.get_visible()
        
        lgl.set_alpha(1.0 if vis else 0.2)
        axl.set_visible(vis)
        self.ax.figure.canvas.draw()
    
    def refresh_map(self, lines: list[Line]):
        """Update legend and legend line mapping
        NOTE: Assumes lines are in same order as legend"""
        # FIXME performance reinstantiating legend
        self.ax.legend(loc='upper left')
        self.lines.clear()
        for lgl, axl in zip(self.ax.get_legend().get_lines(), lines):
            lgl.set_picker(5)
            self.lines[lgl] = axl
    
    def clear(self):
        """remove legend from graph"""
        if self.ax.get_legend():
            self.ax.get_legend().remove()

class LimitHandler:
    """Tracks graph bounds and handles 
    updates to limits of the graph."""
    def __init__(self, ax: plt.Axes, width):
        self.ax = ax
        self.xmax = None
        self.xmin = None
        self.ymax = None
        self.ymin = None
        self.width = width
        self.cur_x = None  # halfway of upper & lower
        
    def set_width(self, width):
        self.width = width
        # new width using current x
        if self.cur_x:
            x = self.cur_x
            dt = self.width//2
            lower, upper = self._bounded(x-dt, x+dt)
            self._set_xlim(lower, upper)
        
    def track_data(self, x, y):
        """Compare new x, y values to tracked 
        limits,update limits if necessary."""
        if self.ymax is None or y > self.ymax:
            self.ymax = y
        if self.ymin is None or y < self.ymin:
            self.ymin = y
        if self.xmax is None or x > self.xmax:
            self.xmax = x
        if self.xmin is None or x < self.xmin:
            self.xmin = x
            
    def clear_tracked(self):
        """Clear all tracked data."""
        self.xmax = None
        self.xmin = None
        self.ymax = None
        self.ymin = None
            
    def set_ylim(self, upper=None, lower=None):
        """Sets the y-axis limits to provided, 
        else, tracked limits are used."""
        if upper is None:
            upper = self.ymax
        if lower is None:
            lower = self.ymin
        if upper or lower:
            self.ax.set_ylim(lower, upper) 
    
    def set_xlim_to_relx(self, percent: float):
        """View graph at relative x between  0.0 (xmin) and 1.0 (xmax)."""
        if self.xmax is None or self.xmin is None:
            return
        x = self._relx_to_x(percent)
        dt = self.width//2
        lower, upper = self._bounded(x-dt, x+dt)
        self._set_xlim(lower, upper)
        
    def set_xlim_to_newest(self):
        """Set the x-axis limits to view the newest data."""
        if self.xmax is None or self.xmin is None:
            return
        lower, upper = self._bounded(self.xmax-self.width, self.xmax)
        self._set_xlim(lower, upper)
        
    def _set_xlim(self, lower, upper):
        """Wrapper to set x-axis limits, which also updates cur_x."""
        self.ax.set_xlim(lower, upper)
        self.cur_x = lower + (upper-lower)/2
    
    def _relx_to_x(self, relx: float):
        """Convert relative x (0.0 - 1.0) to a real x position."""
        if relx < 0:
            relx = 0
        elif relx > 1:
            relx = 1
        return self.xmin + (relx * (self.xmax - self.xmin))
                                  
    def _bounded(self, lower, upper):
        """Bound a range between the tracked limits."""
        if lower < self.xmin:
            lower = self.xmin
        if upper > self.xmax:
            upper = self.xmax
        return lower, upper
   