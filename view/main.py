
from view.root import Root
from view.widgets.serial_connector import SerialConnector
from view.widgets.cli import CLI
from view.controls import VSBControls
from view.widgets.led_button import LEDButton
from view.widgets.file_action import FileAction
from view.widgets.live_graph_tk import LiveGraphTk
from view.help import HelpWindow
from tkinter import Button

class View:
    """VSB View"""
    def __init__(self):
        super().__init__()
        self.root = Root()
        self.controls = VSBControls(self.root)
        self.log = FileAction(self.root, text="Log CPI")
        self.cli = CLI(self.root)
        self.serial = SerialConnector(self.root)
        self.graph = LiveGraphTk(self.root, interval=1000)
        self.mode_button = LEDButton(self.root, text="Generic Mode")
        self.help_button = Button(self.root, text="HELP", command=lambda: HelpWindow(self.root))
        self.exit_button = Button(self.root, text="EXIT", command=self.root.on_close)
            
        self.controls.grid(row=0, column=0, sticky="nsew")
        self.log.grid(row=1, column=0, sticky="nsew")
        self.cli.grid(row=2, column=0, sticky="nsew")
        self.serial.grid(row=3, column=0, sticky="nsew")
        self.graph.grid(row=0, column=1, rowspan=3, columnspan=3, sticky="nsew")
        self.mode_button.grid(row=3, column=1, sticky="nsew")
        self.help_button.grid(row=3, column=2, sticky="nsew")
        self.exit_button.grid(row=3, column=3, sticky="nsew")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        
    def start(self):
        self.root.mainloop()
    
    def bind_mode_button(self, func):
        self.mode_button.set_command(func)
    
    def bind_cli_send(self, func):
        self.cli.set_send_func(func)
        
    def bind_connect(self, func):
        self.serial.set_connect_func(func)
    
    def bind_button(self, name, func):
        self.controls.set_button_command(name, func)
        
    def bind_log(self, func):
        self.log.set_command(func)

    def get_cli_entry(self):
        return self.cli.get_entry()
    
    def get_port(self):
        return self.serial.get_port()

    def get_baud(self):
        return self.serial.get_baud()
    
    def get_led(self, name):
        return self.controls.get_led(name)
    
    def clear_cli(self):
        self.cli.clear()
        
    def append_cli(self, data):
        self.cli.insert(data)
        
    def append_graph(self, channel, val):
        self.graph.append(channel, val)
        
    def set_connected(self, is_connected: bool):
        self.serial.set_state(is_connected)
        
    def set_mode(self, is_generic: bool):
        self.mode_button.set_led(is_generic)
    
    def set_led(self, name, state):
        self.controls.set_led(name, state)
        
    def set_button_command(self, name, func):
        self.controls.set_button_command(name, func)

    def set_readout(self, name, readout):
        self.controls.set_readout(name, readout)
