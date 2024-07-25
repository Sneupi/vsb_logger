import tkinter as tk

class WidgetGrid(tk.Frame):
    def __init__(self, master, widget_class: tk.Widget, list2D):
        """costruct a grid of tk.Widget type given
        a 2D list of strings (names) ordered [column][row]"""
        super().__init__(master)
        self.widgets: dict[str, widget_class] = {}
        self.widget_class = widget_class
        
        for col_ndx, col in enumerate(list2D):
            for row_ndx, name in enumerate(col):
                self.widgets[name] = widget_class(self, text=name)
                self.widgets[name].grid(row=row_ndx, column=col_ndx, sticky='nsew')
                self.rowconfigure(row_ndx, weight=1)
                self.columnconfigure(col_ndx, weight=1)
    
    def get_widgets(self) -> dict:
        return self.widgets
    
    def get_widget(self, name: str):
        return self.widgets.get(name, None)
    
    def get_names(self) -> tuple:
        return tuple(self.get_widgets().keys())

from .led_button import LEDButton
class LEDGrid(WidgetGrid):
    """Widget grid of LEDButtons"""
    def __init__(self, master, list2D):
        super().__init__(master, LEDButton, list2D)
    
    def get_led(self, name: str):
        led = self.get_widget(name)
        if led and isinstance(led, LEDButton):
            return led.get_led()
        return None
    
    def set_led(self, name: str, state: bool):
        led = self.get_widget(name)
        if led and isinstance(led, LEDButton):
            led.set_led(state)
            
    def set_command(self, name: str, func):
        led = self.get_widget(name)
        if led and isinstance(led, LEDButton):
            led.set_command(func)

from .status_box import StatusBox       
class StatusGrid(WidgetGrid):
    """Widget grid of StatusBoxes"""
    def __init__(self, master, list2D):
        super().__init__(master, StatusBox, list2D)
        
    def set_readout(self, name: str, readout: str):
        status = self.get_widget(name)
        if status and isinstance(status, StatusBox):
            status.set_readout(readout)