import tkinter as tk
from .led_button import LEDButton
from tkinter import filedialog

class FileAction(tk.Frame):
    """Generic file browser Frame for selecting a 
    file and performing a specific action on it."""
    def __init__(self, master, text="[Action]", toggle_func=None):
        super().__init__(master)
        super().configure(width=600, height=50)
        self.log_label = tk.Label(self, text="File:")
        self.log_label.place(relx=0.3, rely=0, relwidth=0.1, relheight=1)
        
        self.browse_button = tk.Button(self, text="Select File", command=self.select_file)
        self.browse_button.place(relx=0.15, rely=0, relwidth=0.15, relheight=1)
        
        self.action_button = LEDButton(self, text=text)
        self.action_button.place(relx=0, rely=0, relwidth=0.15, relheight=1)
        
        self.label = tk.Label(self, borderwidth=2, relief="groove")
        self.label.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)
        
    def select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.label.config(text=path)
        
    def set_button_state(self, turn_on: bool):
        """Set state of GUI action button"""
        self.action_button.set_led(turn_on)
        
    def get_button_state(self) -> bool:
        """Get state of GUI action button"""
        return self.action_button.get_led()
        
    def set_command(self, func):
        """Set command function for action button"""
        self.action_button.set_command(func)
            
    def get_path(self):
        return self.label.cget("text")
