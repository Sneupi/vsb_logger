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
            
        sub = self.lines[line_name]  # Sub-dictionary
        sub['x'].append(x)
        sub['y'].append(y)
        sub['line'].set_data(sub['x'], sub['y'])
        
    def put_data(self, channel, time, value):
        """Standardized function to put data into queue."""
        self.data_queue.put((channel, time, value))

    def get_data(self):
        """Standardized function to get data from queue."""
        return self.data_queue.get()
    
    def init(self):
        """Init function for FuncAnimation."""
        self.ax.set_ylim(0, self.Y_HEIGHT)
        self.ax.set_xlim(0, self.X_WIDTH)
        del self.xdata[:]
        del self.ydata[:]
        self.line.set_data(self.xdata, self.ydata)
        return self.line,

    def update(self, val):
        if not self.auto_shift:
            
            if len(self.xdata) > 1:
                mx = max(self.xdata)
                mn = min(self.xdata)
                pos = mn + (self.spos.val * (mx - mn))
                self.ax.set_xlim(pos-self.X_WIDTH//2,pos+self.X_WIDTH//2)
                self.ax.figure.canvas.draw()
            
    def run(self, data):
        """Intake data from queue to update graph."""
        xmin, xmax = self.ax.get_xlim()
        
        while not self.data_queue.empty():
            channel, time, value = self.get_data()
            
            self.xdata.append(time)
            self.ydata.append(value)
        
        if len(self.xdata) != 0:
            mx = max(self.xdata)
            if self.auto_shift and mx >= xmax:
                self.ax.set_xlim(mx-self.X_WIDTH, mx)
                self.ax.figure.canvas.draw()
                
            self.line.set_data(self.xdata, self.ydata)

        return self.line,
    
    def setup_widgets(self):
        """Setup the widgets for the Tkinter frame."""

        def toggle_auto_shift():
            self.auto_shift = not self.auto_shift
            self.auto_shift_button.config(text="Enable Scroller" if self.auto_shift else "Enable Auto-Shift")
            if not self.auto_shift:
                self.update(0)  # Update with current slider value

        def clear_data():
            del self.xdata[:]
            del self.ydata[:]
            
        self.config(width=500, height=500)  # basic size
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=0.95)
                
        self.auto_shift_button = tk.Button(self, text="Enable Scroller", command=toggle_auto_shift)
        self.auto_shift_button.place(relx=0, rely=0.95, relwidth=0.2, relheight=0.05)
            
        self.clear_graph_button = tk.Button(self, text="Clear Graph", command=clear_data)
        self.clear_graph_button.place(relx=0.2, rely=0.95, relwidth=0.2, relheight=0.05)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.toolbar.place(relx=0.4, rely=0.95, relwidth=0.6, relheight=0.05)


if __name__ == "__main__":
    """Demo of the LiveGraphFrame class."""
    
    import threading
    import time
    import random
    
    def dummy_data_thread(graph: LiveGraphFrame):
        """Simulate graphing data coming in from a queue."""
        while True:
            for i in range(12):
                graph.put_data(i, time.time_ns()/1e9, random.randint(0, 4095))
                time.sleep(0.07)
    
    root = tk.Tk()
    
    lgf = LiveGraphFrame(root)
    lgf.pack()
    
    thread = threading.Thread(target=dummy_data_thread, args=(lgf,))
    thread.daemon = True
    thread.start()
    
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit() or root.destroy())
    root.mainloop()
    
    print("DEMO END")