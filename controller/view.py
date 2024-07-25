
from view.root import Root
from view.widgets.serial_connector import SerialConnector
from view.widgets.cli import CLI
from view.controls import VSBControls

class TestView:
    def __init__(self):
        super().__init__()
        self.root = Root()
        self.cli = CLI(self.root)
        self.controls = VSBControls(self.root)
        self.serial = SerialConnector(self.root)
        
        self.controls.grid(row=0, column=0)
        self.cli.grid(row=1, column=0)
        self.serial.grid(row=2, column=0)
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def start(self):
        self.root.mainloop()
        
    def bind_cli_send(self, func):
        self.cli.set_send_func(func)
        
    def bind_connect(self, func):
        self.serial.set_connect_func(func)
    
    def bind_button(self, name, func):
        self.controls.set_button_command(name, func)

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
        
    def set_connected(self, is_connected: bool):
        self.serial.set_state(is_connected)
    
    def set_led(self, name, state):
        self.controls.set_led(name, state)
        
    def set_button_command(self, name, func):
        self.controls.set_button_command(name, func)

