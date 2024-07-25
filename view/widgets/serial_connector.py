import tkinter as tk
import tkinter.ttk as ttk
from .led_button import LEDButton
import serial.tools.list_ports

class SerialConnector(tk.Frame):
    """User interface for setting up serial connection"""
    def __init__(self, parent):
        super().__init__(parent)
        
        self.port_label = tk.Label(self, text="Port:")
        self.port_label.pack(side='left', padx=5, pady=5)
        
        self.port_options = self.get_available_ports()
        self.port_var = tk.StringVar(self)
        if self.port_options:
            self.port_var.set(self.port_options[0])
        self.port_dropdown = ttk.Combobox(self, textvariable=self.port_var, values=self.port_options)
        self.port_dropdown.pack(side='left', padx=5, pady=5)
        
        self.baud_label = tk.Label(self, text="Baud:")
        self.baud_label.pack(side='left', padx=5, pady=5)

        self.baud_options = ['9600', '19200', '38400', '57600', '115200']
        self.baud_var = tk.StringVar(self)
        self.baud_var.set(self.baud_options[4])
        self.baud_dropdown = ttk.Combobox(self, textvariable=self.baud_var, values=self.baud_options)
        self.baud_dropdown.pack(side='left', padx=5, pady=5)
        
        self.refresh_button = tk.Button(self, text="Refresh Ports", command=self.refresh_ports)
        self.refresh_button.pack(side='right', padx=5, pady=5)
    
        self.connect_button = LEDButton(self, text="Connect")
        self.connect_button.pack(side='right', padx=5, pady=5, fill='both', expand=True)
        
    def set_connect_func(self, func):
        self.connect_button.set_command(command=func)
    
    def get_available_ports(self):
        """Get system available serial port names as list"""
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.device)
        return ports
    
    def get_port(self):
        """Get selected port name string"""
        return self.port_var.get()
    
    def get_baud(self):
        """Get selected baud rate string"""
        return self.baud_var.get()

    def set_state(self, is_connected: bool):
        """Set connection status LED on connect button"""
        self.connect_button.set_led(is_connected)
    
    def refresh_ports(self):
        """Update dropdown with available ports"""
        self.port_options = self.get_available_ports()
        self.port_dropdown['values'] = self.port_options
