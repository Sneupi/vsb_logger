"""Package containing classes for live 
matplotlib graphs with interactive interface."""

from .helpers import LinesHandler, LimitHandler
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class LiveGraph:
    """Live matplotlib graph with interactive interface."""
    def __init__(self, width, interval=500, enable_pick_event=True):
        """NOTE: units/type of x must be consistent for all provided values.
        
        Args:
            width (Any): Width of the graph in x-axis units
            interval (int): Refresh interval millis.
        """
        self.fig, self.ax = plt.subplots()
        self.ax.grid()
        self.ax.tick_params(axis='x', rotation=45)
        self.fig.subplots_adjust(bottom=0.2)
        
        self.lines = LinesHandler(self.ax, self.fig, enable_pick_event)
        self.ani = FuncAnimation(self.fig, self._run, blit=False, 
                                 interval=interval, repeat=False)
        self.limits = LimitHandler(self.ax, width)
        self.is_auto = True
        
    def append(self, line_name, x, y):
        """Append data to the graph at line"""
        self.limits.track_data(x, y)
        self.lines.append(line_name, x, y)
        
    def set_width(self, width):
        """Set the width of the graph in x-axis units."""
        self.limits.set_width(width)
        self.fig.canvas.draw_idle()
    
    def set_auto(self, is_auto):
        """Set the graph to autoshift mode, else
        x-axis remains still until manually updated"""
        self.is_auto = is_auto
    
    def set_xlim_to_relx(self, percent: float):
        """View graph at relative x between 0.0 (xmin) and 1.0 (xmax)."""
        self.limits.set_xlim_to_relx(percent)
        self.fig.canvas.draw_idle()
        
    def clear(self):
        """Clear all lines from graph"""
        self.lines.clear_all()
        self.limits.clear_tracked()
        self.fig.canvas.draw_idle()
    
    def _run(self, _):
        # Update bounds
        if self.is_auto:
            self.limits.set_xlim_to_newest()
        self.limits.set_ylim()
        # Update lines
        return self.lines.get_lines()

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import datetime

class LiveGraphTk(tk.Frame):
    """Generic tkinter.Frame LiveGraph using graph.LiveGraph.
    
    NOTE: This example enforces datetime units of width."""
        
    def append(self, line_name, y):
        x = datetime.datetime.now()
        self.graph.append(line_name, x, y)
        
    def __init__(self, master, interval):
        super().__init__(master)
        
        def toggle_auto():
            self.graph.set_auto(not self.graph.is_auto)
            txt = "Autoshift " + ("ON" if self.graph.is_auto else "OFF")
            self.auto_button.config(text=txt)
        
        def manual_scroll(event):
            if self.graph.is_auto:
                return
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
        
