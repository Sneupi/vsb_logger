"""
File: gui.py
Author: Gabe Venegas
Purpose: File containing VSB GUI class
"""

import tkinter as tk
import tkpanels as tkp

class VSBGUI(tk.Tk):
    """GUI frontend for VSB logger & plotter"""
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title("VSB Logger")
        self.geometry("1400x700")
        self.resizable(False, False)

        self.controls = tkp.ControlsFrame(self)
        self.controls.place(relx=0, rely=0, relwidth=0.45, relheight=0.3)
        
        self.filebrowser = tkp.FileBrowser(self)
        self.filebrowser.place(relx=0, rely=0.3, relwidth=0.45, relheight=0.05)
                
        self.serial_setup = tkp.SerialSetup(self)
        self.serial_setup.place(relx=0, rely=0.95, relwidth=0.45, relheight=0.05)

        self.terminal = tkp.CLIFrame(self)
        self.terminal.place(relx=0.01, rely=0.36, relwidth=0.43, relheight=0.58)
        
        # TODO Graph
        # TODO Graph scroll
        # TODO Data clear
    
    def bind_control(self, widget_name, func):
        """Bind function to a GUI control panel button."""
        self.controls.bind_func(widget_name, func)

    def update_control(self, widget_name, data):
        """Update widget on control panel with new data."""
        self.controls.set_data(widget_name, data)
        
    def terminal_insert(self, data):
        """Insert data into terminal."""
        self.terminal.insert(data)
        
    def update_graph(self, tuple_list):
        """Update graph with new data.
        Accepts a list of tuples (x, y)."""
        pass  # TODO

if __name__ == "__main__":
    app = VSBGUI()
    app.mainloop()