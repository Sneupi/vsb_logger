"""Package for the GUI frontend of the VSB logger & plotter."""

import tkinter as tk
from .helpers import VSBPanelFrame, FileBrowser, SerialSetup, CLIFrame, \
                        VSBHelpTopLevel, ControlPair, StatePair
from .graphing import LiveGraphTk

class VSBView(tk.Tk):
    """GUI frontend for VSB logger & plotter"""
    
    def __init__(self, interval, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("VSB Logger")
        self.geometry("1400x700")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: self.quit() or self.destroy())
        
        self.cv_mode = True

        self.controls = VSBPanelFrame(self)
        self.controls.place(relx=0, rely=0, relwidth=0.45, relheight=0.28)
        
        self.filebrowser = FileBrowser(self, action_name="Log CPI")
        self.filebrowser.place(relx=0, rely=0.29, relwidth=0.45, relheight=0.06)

        self.serial_setup = SerialSetup(self)
        self.serial_setup.place(relx=0, rely=0.95, relwidth=0.45, relheight=0.05)

        self.terminal = CLIFrame(self)
        self.terminal.place(relx=0.01, rely=0.36, relwidth=0.43, relheight=0.58)
        
        self.graph = LiveGraphTk(self, interval)
        self.graph.place(relx=0.45, rely=0.05, relwidth=0.55, relheight=0.95)
        
        self.help_button = tk.Button(self, text="HELP", command=self.spawn_help)
        self.help_button.place(relx=0.8, rely=0, relwidth=0.1, relheight=0.05)
        
        self.exit_button = tk.Button(self, text="EXIT")
        self.exit_button.place(relx=0.9, rely=0, relwidth=0.1, relheight=0.05)
        self.exit_button.config(command=lambda: self.quit() or self.destroy())
        
        self.controlpair_dict: dict[str, ControlPair]= dict()
        self.controlpair_dict.update(self.controls.get_controlpairs())
        self.controlpair_dict.update({self.filebrowser.name: self.filebrowser.action_button})
        self.controlpair_dict.update({self.serial_setup.connect_name: self.serial_setup.connect_button})
        
        self.statepair_dict: dict[str, StatePair] = dict()
        self.statepair_dict.update(self.controls.get_statepairs())
    
    def start(self):
        """Start the GUI"""
        self.mainloop()
        
    def __del__(self):
        self.graph.quit() or self.graph.destroy()
    
    def spawn_help(self):
        """Spawn a help window"""
        help_window = VSBHelpTopLevel(self)

    def set_command(self, name, func):
        """Set the command of a control pair button"""
        ctrl = self.controlpair_dict.get(name, None)
        if ctrl:
            ctrl.config(command=func)
    
    def set_terminal_send(self, func):
        """Set the function called on <Return> in the terminal"""
        self.terminal.set_send_func(func)
    
    def set_led(self, name, state):
        """Set the LED state of a control pair"""
        ctrl = self.controlpair_dict.get(name, None)
        if ctrl:
            ctrl.config(led=state)
    
    def set_readout(self, name, text):
        """Set the text of a state pair readout"""
        stat = self.statepair_dict.get(name, None)
        if stat:
            stat.config(readout_text=text)
    
    def append_terminal(self, data: str):
        """Append a message to the terminal"""
        self.terminal.insert(data)
        
    def append_graph(self, ch, val):
        """Append data to the graph"""
        self.graph.append(ch, val)
            
    def get_terminal_entry(self):
        """Get the terminal entry"""
        return self.terminal.get_entry()
    
    def get_log_path(self):
        """Get the log file path"""
        return self.filebrowser.get_path()
    
    def get_port(self):
        """Get the selected port"""
        return self.serial_setup.get_port()
    
    def get_baud(self):
        """Get the selected baud rate"""
        return self.serial_setup.get_baud()
    
    def get_led(self, name):
        """Get the LED state of a control pair"""
        ctrl = self.controlpair_dict.get(name, None)
        if ctrl:
            return ctrl.get_led()
        return None