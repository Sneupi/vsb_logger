"""Package for the GUI frontend of the VSB logger & plotter."""

from typing import TypedDict
import tkinter as tk
from .root import Root

from .help import HelpView
from .controls import ControlsView
from .log import LogView
from .cli import CLIView
from .serialview import SerialView
from .graph import GraphView

class View:
    """GUI frontend for VSB logger & plotter"""
    
    def __init__(self):
        super().__init__()
        self.root = Root()

        self.controls = ControlsView(self.root)
        self.controls.place(relx=0, rely=0, relwidth=0.45, relheight=0.28)
        
        self.log = LogView(self.root)
        self.log.place(relx=0, rely=0.29, relwidth=0.45, relheight=0.06)

        self.serial = SerialView(self.root)
        self.serial.place(relx=0, rely=0.95, relwidth=0.45, relheight=0.05)

        self.cli = CLIView(self.root)
        self.cli.place(relx=0.01, rely=0.36, relwidth=0.43, relheight=0.58)
        
        self.graph = GraphView(self.root)
        self.graph.place(relx=0.45, rely=0.05, relwidth=0.55, relheight=0.95)
        
        self.help_button = tk.Button(self.root, text="HELP", command=lambda: HelpView(self.root))
        self.help_button.place(relx=0.8, rely=0, relwidth=0.1, relheight=0.05)
        
        self.exit_button = tk.Button(self.root, text="EXIT")
        self.exit_button.place(relx=0.9, rely=0, relwidth=0.1, relheight=0.05)
        self.exit_button.config(command=self.root.on_close)
            
    def start(self):
        """Start the GUI"""
        self.root.mainloop()