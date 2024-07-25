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