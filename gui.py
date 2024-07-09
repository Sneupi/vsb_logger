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
    
    def bind_control(self, name, func):
        """Bind function to a GUI control (button, etc).
        
        Valid names:
        - #TODO"""
        pass  # TODO

    def update_widget(self, name, data):
        """Update GUI widget with new data.
        Must be valid datatype per widget, 
        else TypeError.
        
        Datatypes:
        - Status: str
        - Button: bool
        - Terminal: str
        - Graph: list of tuples (x, y)
        
        Valid names:
        - #TODO"""
        pass  # TODO

if __name__ == "__main__":
    app = VSBGUI()
    app.mainloop()