
import tkinter as tk
from .widgets.status_frame import StatusFrame
from .widgets.led_button import LEDButton
from .widgets.widget_grid import WidgetGrid

class ControlsView(tk.Frame):
    """View for controls panel of VSB (Voltage Sense & Balancing) """
    def __init__(self, master):
        super().__init__(master)
        
        
        # list[column][row] of each type
        ctrl_names = [["Run", "Stop", "Balance", "ExtBus", "MQ Dump", "Show DN"], 
                      ["Debug", "Debug2", "Trace", "Trace2", "Info", "Error"]]
        stat_names = [["PVM", "CTC", "Last CV", "Last CV DN", "Last Err", "Errs"]]
        
        self.but_grid = WidgetGrid(self, LEDButton, ctrl_names)
        self.but_grid.pack(side='left', fill='both', expand=True)
        self.stat_grid = WidgetGrid(self, StatusFrame, stat_names)  
        self.stat_grid.pack(side='left', fill='both', expand=True)
        
    def get_ledbutton(self) -> dict:
        return self.but_grid.get_widgets()
    
    def get_statusframe(self) -> dict:
        return self.stat_grid.get_widgets()
    
    def set_button_command(self, button_name, func):
        button = self.but_grid.get_widgets().get(button_name, None)
        if button:
            button.set_command(func)

