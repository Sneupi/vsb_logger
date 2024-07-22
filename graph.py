"""
File: graph.py
Author: Gabe Venegas
Purpose: Live matplotlib graph with interactive interface.
Also provides a working interface LiveGraphFrame using tkinter.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import datetime

class Line:
    """Line object to abstract matplotlib Line2D management"""
    def __init__(self, name, ax: plt.Axes):
        self.x = []
        self.y = []
        self.line = ax.plot([], [], label=name)[0]
            
    def append(self, x, y):
        """Append a data point to line and update the plot.
        If the legend line is hidden, unhide legend line."""
        self.x.append(x)
        self.y.append(y)
        self.line.set_data(self.x, self.y)
        
    def __del__(self):
        self.line.remove()
        
class LinesHandler:
    """Structure to hold & manage multiple Line objects.
    
    NOTE: This class takes over 'pick_event' handling
    for the figure to allow toggle visibility of lines."""
    def __init__(self, ax: plt.Axes, fig: plt.Figure):
        self.ax = ax
        self.line_dict = dict()  # map str(name) to Line()
        self.leg_dict = dict()  # map Line2D(legend) to Line2D(ax)
        
        # Set pick event to toggle visibility of lines
        fig.canvas.mpl_connect('pick_event', self.on_pick)
        
    def on_pick(self, event):
        """Toggle the visibility of the original line
        corresponding to the legend proxy line."""
        legline = event.artist
        if legline not in self.leg_dict:
            return
        axline = self.leg_dict[legline]
        vis = not axline.get_visible()
        axline.set_visible(vis)
        legline.set_alpha(1.0 if vis else 0.2)
        self.ax.figure.canvas.draw()
        
    def get_lines(self):
        """Return list of matplotlib Line2D objects."""
        return [ln.line for ln in self.line_dict.values()]
    
    def _refresh_legend_map(self):
        """Update the legend line dict to the new legend line addresses."""
        self.leg_dict.clear()
        for legline in self.ax.get_legend().get_lines():
            # pick radius of 5
            legline.set_picker(5)  
            # Map legend line to ax line
            lbl = legline.get_label()
            self.leg_dict[legline] = self.line_dict[lbl].line
    
    def append(self, nm, x, y):
        """Append data to a line, creating a new line if necessary.
        If the line is new, create a new line on the plot, and 
        update/create the legend."""
        if nm not in self.line_dict:
            # Create new Line (..creates new Line2D on plot)
            self.line_dict[nm] = Line(nm, self.ax)
            # Instantiate updated legend
            self.ax.legend(loc='upper left')
            self.ax.get_legend().set_draggable(True)
            # Refresh legend map with new line addresses
            self._refresh_legend_map()
        self.line_dict[nm].append(x, y)
        
    def clear_all(self):
        """Delete Line objects (deleting 
        Line2D obj) and clear dict"""
        self.line_dict.clear()
            
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
        # update xlim to new width, using current x position
        if self.cur_x:
            x = self.cur_x
            dt = self.width//2
            lower, upper = self._bounded(x-dt, x+dt)
            self._set_xlim(lower, upper)
        
    def track_data(self, x, y):
        """Compare new x, y values to tracked limits,
        update limits if necessary."""
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
        """Sets the y-axis limits to view the graph between
        the provided upper and lower bounds. If not provided,
        the tracked limits are used."""
        if upper is None:
            upper = self.ymax
        if lower is None:
            lower = self.ymin
        if upper or lower:
            self.ax.set_ylim(lower, upper) 
    
    def set_xlim_to_relx(self, percent: float):
        """Move the view to a relative x along the 
        graph. 0.0 being the leftmost point, 1.0 
        being the rightmost data point"""
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
        """Wrapper for setting x-axis limits.
        Also updates the current x position."""
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
    
class LiveGraph:
    """Live matplotlib graph with interactive interface."""
    def __init__(self, width, interval=500):
        """Note: Width may be any type that supports 
        addition and division andfor matplotlib graphing
        
        Args:
            width (Any): Width of the graph in x-axis units
            interval (int): Refresh interval millis.
        """
        self.fig, self.ax = plt.subplots()
        self.ax.grid()
        self.ax.tick_params(axis='x', rotation=45)
        self.fig.subplots_adjust(bottom=0.2)
        
        self.lines = LinesHandler(self.ax, self.fig)
        self.ani = FuncAnimation(self.fig, self._run, blit=False, 
                                 interval=interval, repeat=False)
        self.limits = LimitHandler(self.ax, width)
        self.is_auto = True
        
    def append(self, line_name, x, y):
        self.limits.track_data(x, y)
        self.lines.append(line_name, x, y)
        
    def set_width(self, width):
        """Set the width of the graph in x-axis units."""
        self.limits.set_width(width)
    
    def set_auto(self, is_auto):
        """Set the graph to automatically shift to the newest data.
        Else, the graph will stay at the current view."""
        self.is_auto = is_auto
    
    def set_xlim_to_relx(self, percent: float):
        """Move the view to a relative x along the 
        graph. 0.0 being the leftmost point, 1.0 
        being the rightmost data point"""
        self.limits.set_xlim_to_relx(percent)
        
    def clear(self):
        self.lines.clear_all()
        self.limits.clear_tracked()
    
    def _run(self, _):
        # Update bounds
        if self.is_auto:
            self.limits.set_xlim_to_newest()
        self.limits.set_ylim()
        # Update lines
        return self.lines.get_lines()

class LiveGraphFrame(tk.Frame):
    """Generic tkinter.Frame interface for LiveGraph class.
    
    NOTE: This example enforces datetime units of width."""
        
    def append(self, line_name, y):
        x = datetime.datetime.now()
        self.graph.append(line_name, x, y)
        
    def __init__(self, master, interval=100):
        super().__init__(master)
        
        def toggle_auto():
            self.graph.set_auto(not self.graph.is_auto)
            txt = "Autoshift " + ("ON" if self.graph.is_auto else "OFF")
            self.auto_button.config(text=txt)
        
        def manual_scroll(event):
            self.graph.set_xlim_to_relx(self.scroll_slider.get()/100)
            
        def update_width(event=None):
            time_units = {
                "Seconds": 1,
                "Minutes": 60,
                "Hours": 3600,
                "Days": 86400
            }
            unit = self.unit_var.get()
            width = self.width_slider.get() * time_units[unit]
            self.graph.set_width(datetime.timedelta(seconds=width))
            
        self.graph = LiveGraph(width=datetime.timedelta(seconds=10), interval=interval)
        self.canvas = FigureCanvasTkAgg(self.graph.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=10, sticky=tk.NSEW)
            
        self.auto_button = tk.Button(self, text="Autoshift ON", command=toggle_auto)
        self.auto_button.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        
        self.scroll_slider = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.scroll_slider.bind("<B1-Motion>", manual_scroll)
        self.scroll_slider.grid(row=1, column=2, columnspan=8, sticky=tk.NSEW)
        
        time_units = ["Seconds", "Minutes", "Hours", "Days"]
        self.unit_var = tk.StringVar(self)
        self.unit_var.set(time_units[0])
        self.unit_menu = tk.OptionMenu(self, self.unit_var, *time_units)
        self.unit_menu.grid(row=2, column=0, sticky=tk.NSEW)
        
        self.unit_updater_button = tk.Button(self, text="Update Units", 
                                             command=update_width)
        self.unit_updater_button.grid(row=2, column=1, sticky=tk.NSEW)
        
        self.width_slider = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL)
        self.width_slider.grid(row=2, column=2, columnspan=8, sticky=tk.NSEW)
        self.width_slider.bind("<B1-Motion>", update_width)
        
        self.clear_button = tk.Button(self, text="Clear Graph", command=self.graph.clear)
        self.clear_button.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW)
    
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(row=4, column=0, columnspan=10, sticky=tk.NSEW)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(7, weight=1)
        self.grid_columnconfigure(8, weight=1)
        self.grid_columnconfigure(9, weight=1)

def __demo_tkinter():
    import threading
    import time
    import datetime
    import random
    
    def thread_func(graph: LiveGraphFrame):
        """Simulate graphing data coming in from a source"""
        while True:
            for i in range(12):
                v = random.randint(341*i, 341*(i+1))
                graph.append(f"{i}", v)
                time.sleep(0.07)
    
    root = tk.Tk()
    gph = LiveGraphFrame(root)
    gph.pack(fill=tk.BOTH, expand=True)
                
    thread = threading.Thread(target=thread_func, args=(gph,))
    thread.daemon = True
    thread.start()
    
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit() or root.destroy())
    root.mainloop()

def __demo_random():
    """
    - Using random data
    - Using datetime x-axis
    - Using interval of 100ms"""
    import threading
    import time
    import datetime
    import random
    
    def thread_func(graph: LiveGraph):
        """Simulate graphing data coming in from a source"""
        while True:
            for i in range(12):
                t = datetime.datetime.now()
                v = random.randint(341*i, 341*(i+1))
                graph.append(f"{i}", t, v)
                time.sleep(0.07)
                
    lgf = LiveGraph(interval=100, width=datetime.timedelta(seconds=10))
    
    thread = threading.Thread(target=thread_func, args=(lgf,))
    thread.daemon = True
    thread.start()
    
    plt.show()
    
    print("DEMO END")
    
def __demo_waves():
    """
    - Using sine waves
    - Using time (convert to float seconds)
    - Using interval of 1000ms"""
    import threading
    import time
    import numpy as np
    
    def thread_func(graph: LiveGraph):
        while True:
            for i in range(12):
                t = time.time_ns()/1e9
                # t = datetime.datetime.now()
                v = (np.sin(t) + i) * 4095/12
                graph.append(f"{i}", t, v)
                time.sleep(0.07)
            
    lgf = LiveGraph(interval=1000, width=5)
    thread = threading.Thread(target=thread_func, args=(lgf,))
    thread.daemon = True
    thread.start()
    plt.show()
    
    print("DEMO END")

if __name__ == "__main__":
    # __demo_random()
    # __demo_waves()
    __demo_tkinter()