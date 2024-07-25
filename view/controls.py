
import tkinter as tk
from .widgets.status_frame import StatusFrame
from .widgets.led_button import LEDButton
from .widgets.widget_grid import WidgetGrid

class ControlsView(tk.Frame):
    """View for controls panel of VSB (Voltage Sense & Balancing) """
    def __init__(self, master):
        super().__init__(master)
        
        
        # list[column][row] of each type
        self.ctrl_names = [["Run", "Stop", "Balance", "ExtBus", "MQ Dump", "Show DN"], 
                      ["Debug", "Debug2", "Trace", "Trace2", "Info", "Error"]]
        self.stat_names = [["PVM", "CTC", "Last CV", "Last CV DN", "Last Err", "Errs"]]
        
        self.but_grid = WidgetGrid(self, LEDButton, self.ctrl_names)
        self.but_grid.pack(side='left', fill='both', expand=True)
        self.stat_grid = WidgetGrid(self, StatusFrame, self.stat_names)  
        self.stat_grid.pack(side='left', fill='both', expand=True)
        
    def get_buttons(self) -> dict:
        """As dictionary of name: LEDButton"""
        return self.but_grid.get_widgets()
        
    def get_statuses(self) -> dict:
        """As dictionary of name: StatusFrame"""
        return self.stat_grid.get_widgets()
    
    def set_readout(self, name, string):
        status = self.stat_grid.get_widget(name)
        if status and isinstance(status, StatusFrame):
            status.set_readout(string)

    def set_led(self, name, state):
        button = self.but_grid.get_widget(name)
        if button and isinstance(button, LEDButton):
            button.set_led(state)
    
    def get_led(self, name):
        button = self.but_grid.get_widget(name)
        if button and isinstance(button, LEDButton):
            return button.get_led()
        return None
            
    def set_button_command(self, button_name, func):
        button = self.but_grid.get_widget(button_name)
        if button and isinstance(button, LEDButton):
            button.set_command(func)

