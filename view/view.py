"""Package for the GUI frontend of the VSB logger & plotter."""

import tkinter as tk
from .root import Root

from .help import HelpWindow
from .controls import VSBControls
from .widgets.file_action import FileAction

from .widgets.cli import CLI
from .widgets.serial_connector import SerialConnector
from .widgets.live_graph_tk import LiveGraphTk

class View:
    """GUI frontend for VSB logger & plotter"""
    
    def __init__(self):
        super().__init__()
        GRAPH_INTERVAL = 1000
        self.root = Root()

        self.controls_view = VSBControls(self.root)
        self.controls_view.place(relx=0, rely=0, relwidth=0.45, relheight=0.28)
        
        self.log_view = FileAction(self.root, text="Log CPI")
        self.log_view.place(relx=0, rely=0.29, relwidth=0.45, relheight=0.06)

        self.serial_view = SerialConnector(self.root)
        self.serial_view.place(relx=0, rely=0.95, relwidth=0.45, relheight=0.05)

        self.cli_view = CLI(self.root)
        self.cli_view.place(relx=0.01, rely=0.36, relwidth=0.43, relheight=0.58)
        
        self.graph_view = LiveGraphTk(self.root, interval=GRAPH_INTERVAL)
        self.graph_view.place(relx=0.45, rely=0.05, relwidth=0.55, relheight=0.95)
        
        self.help_button = tk.Button(self.root, text="HELP", command=lambda: HelpWindow(self.root))
        self.help_button.place(relx=0.8, rely=0, relwidth=0.1, relheight=0.05)
        
        self.exit_button = tk.Button(self.root, text="EXIT")
        self.exit_button.place(relx=0.9, rely=0, relwidth=0.1, relheight=0.05)
        self.exit_button.config(command=self.root.on_close)
            
    def start(self):
        """Start the GUI"""
        self.root.mainloop()