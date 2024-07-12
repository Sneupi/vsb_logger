import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import queue

class LiveGraphFrame(tk.Frame):
    def __init__(self, master, x_width=10, y_height=4095, refresh_ms=500):
        super().__init__(master)
        
        # Constants
        self.X_WIDTH = x_width
        self.Y_HEIGHT = y_height
        self.REFRESH_MS = refresh_ms
        
        # Matplotlib
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)
        self.line, = self.ax.plot([], [], lw=2)
        self.lines = dict()
        self.map_legend_to_ax = dict()
        self.ax.grid()
        self.xdata, self.ydata = [], []
        self.ani = animation.FuncAnimation(self.fig, self.run, blit=False, interval=self.REFRESH_MS,
                                    repeat=False, init_func=self.init)
        
        # Slider (Matplotlib)
        self.axcolor = 'lightgoldenrodyellow'
        self.axpos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=self.axcolor)
        self.spos = Slider(self.axpos, 'Pos', 0, 1)
        self.spos.on_changed(self.update)

        # Other
        self.data_queue = queue.Queue()
        self.auto_shift = True
        
        self.setup_widgets()

    def add_datapoint(self, line_name, x: int, y: int):
        """Internal function for updating the 
        lines dict with a new data point."""
        if line_name not in self.lines:
            self.lines[line_name] = {
                'line': self.ax.plot([], [], label=line_name)[0], 
                'x': [], 
                'y': []
            }
            if len(self.lines) % 12 == 0:  # FIXME: Hardcoded number & bad code placement
                leg = self.ax.legend(loc='upper left')  # Create legend once every 12 lines
                for legend_line, ax_line in zip(leg.get_lines(), self.get_all_lines()):
                    legend_line.set_picker(5)  # pick radius of 5
                    self.map_legend_to_ax[legend_line] = ax_line
            
        sub = self.lines[line_name]  # Sub-dictionary
        sub['x'].append(x)
        sub['y'].append(y)
        sub['line'].set_data(sub['x'], sub['y'])
        
    def on_pick(self, event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in self.map_legend_to_ax:
            return

        ax_line = self.map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        self.fig.canvas.draw()
        
    def get_xdata(self, line_name):
        """Get the xdata for a specific line."""
        return self.lines[line_name]['x']
    
    def get_all_xdata(self):
        """Get combined list of all xdata from all lines."""
        return [x for sublist in [d['x'] for d in self.lines.values()] for x in sublist]
    
    def get_ydata(self, line_name):
        """Get the ydata for a specific line."""
        return self.lines[line_name]['y']
    
    def get_all_lines(self):
        """Get all line objects from the lines dict."""
        return (d['line'] for d in self.lines.values())
            
    def put_data(self, channel, time, value):
        """Standardized function to put data into queue."""
        self.data_queue.put((channel, time, value))

    def get_data(self):
        """Standardized function to get data from queue."""
        return self.data_queue.get()
    
    def clear_all_data(self):
        """Clear a line's data from the graph."""
        for line_name in self.lines.keys():
            del self.lines[line_name]['x'][:]
            del self.lines[line_name]['y'][:]
    
    def init(self):
        """Init function for FuncAnimation."""
        self.ax.set_ylim(0, self.Y_HEIGHT)
        self.ax.set_xlim(0, self.X_WIDTH)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.clear_all_data()
        return self.get_all_lines()

    def update(self, val):
        if not self.auto_shift:
            x = self.get_all_xdata()
            if len(x) > 1:
                mn = min(x)
                pos = mn + (self.spos.val * (max(x) - mn))
                self.ax.set_xlim(pos-self.X_WIDTH//2,pos+self.X_WIDTH//2)
                self.ax.figure.canvas.draw()
            
    def run(self, data):
        """Intake data from queue to update graph."""
        xmin, xmax = self.ax.get_xlim()
        
        while not self.data_queue.empty():
            channel, time, value = self.get_data()
            self.add_datapoint(channel, time, value)
        
        all_x = self.get_all_xdata()
        if len(all_x) > 0:
            mx = max(all_x)
            if self.auto_shift and mx >= xmax:
                self.ax.set_xlim(mx-self.X_WIDTH, mx)
                self.ax.figure.canvas.draw()

        return self.get_all_lines()
    
    def setup_widgets(self):
        """Setup the widgets for the Tkinter frame."""

        def toggle_auto_shift():
            self.auto_shift = not self.auto_shift
            self.auto_shift_button.config(text="Enable Scroller" if self.auto_shift else "Enable Auto-Shift")
            if not self.auto_shift:
                self.update(0)  # Update with current slider value
            
        self.config(width=500, height=500)  # basic size
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=0.95)
                
        self.auto_shift_button = tk.Button(self, text="Enable Scroller", command=toggle_auto_shift)
        self.auto_shift_button.place(relx=0, rely=0.95, relwidth=0.15, relheight=0.05)
            
        self.clear_graph_button = tk.Button(self, text="Clear Graph", command=self.clear_all_data)
        self.clear_graph_button.place(relx=0.15, rely=0.95, relwidth=0.15, relheight=0.05)
        
        self.x_width_label = tk.Label(self, text="x_width:")
        self.x_width_label.place(relx=0.3, rely=0.95, relwidth=0.1, relheight=0.05)
        
        def set_x_width(event):
            try:
                self.X_WIDTH = int(self.x_width_entry.get())
            except ValueError:
                pass
        
        self.x_width_entry = tk.Entry(self)
        self.x_width_entry.insert(0, str(self.X_WIDTH))
        self.x_width_entry.place(relx=0.4, rely=0.95, relwidth=0.1, relheight=0.05)
        self.x_width_entry.bind("<Return>", set_x_width)
            
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.toolbar.place(relx=0.5, rely=0.95, relwidth=0.5, relheight=0.05)


if __name__ == "__main__":
    """Demo of the LiveGraphFrame class."""
    
    import threading
    import time
    import random
    import numpy as np
    
    def dummy_data_thread(graph: LiveGraphFrame):
        """Simulate graphing data coming in from a queue."""
        while True:
            for i in range(12):
                t = time.time_ns()/1e9
                v = (np.sin(t) + i) * 4095/12
                graph.put_data(f"CH{i+1}", t, v)
                time.sleep(0.07)
    
    root = tk.Tk()
    
    lgf = LiveGraphFrame(root, refresh_ms=50)
    lgf.pack(fill=tk.BOTH, expand=True)
    
    thread = threading.Thread(target=dummy_data_thread, args=(lgf,))
    thread.daemon = True
    thread.start()
    
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit() or root.destroy())
    root.mainloop()
    
    print("DEMO END")