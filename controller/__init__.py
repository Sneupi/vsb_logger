import tkinter as tk
from model import SerialModel
from view import VSBView
    
class VSBController:
    """Controller for connection between 
    Model and View of VSB app"""
    pass
        
    
class TestController:
    """Example controller to demonstrate 
    SerialModel and SerialThread"""
    def __init__(self, view: 'TestView'):
        self.model = None
        self.view = view
        
        self.view.bind_send(self._send_data)
        self.view.bind_reconnect(self._reconnect)
    
    def start(self):
        self.view.start()
    
    def _send_data(self, data):
        data = self.view.get_input()
        self.view.clear_input()
        self.model.write(data.strip() + '\n')
        
    def _reconnect(self):
        if self.model:
            self.model.stop()
        try:
            port = self.view.get_port()
            baud = self.view.get_baud()
            self.model = SerialModel(port, int(baud))
            
            self.model.add_event_listener('rx', self._rx_listener)
            self.model.add_event_listener('tx', self._tx_listener)
            self.model.add_event_listener('rx', self._rx_listener_log)
            self.model.add_event_listener('tx', self._tx_listener_log)
            
            self.model.start()
        except Exception as e:
            print(f"SerialController Error: {e}")
            
    def _rx_listener(self, model: SerialModel):
        self.view.append_data(f"RX > {str(model.last_rx).strip()}")
        
    def _tx_listener(self, model: SerialModel):
        self.view.append_data(f"TX > {str(model.last_tx).strip()}")
    
    def _tx_listener_log(self, model: SerialModel):
        print(f"LOGGING TX: {str(model.last_tx).strip()}")
    
    def _rx_listener_log(self, model: SerialModel):
        print(f"LOGGING RX: {str(model.last_rx).strip()}")
        
class TestView(tk.Tk):
    """Example GUI to demonstrate 
    SerialThread and SerialLogger"""
    def __init__(self):
        super().__init__()
        
        class SerialDetails(tk.Frame):
            def __init__(self, master):
                super().__init__(master)
                self.port_label = tk.Label(self, text="Port:")
                self.port_label.pack(side=tk.LEFT)
                self.port_entry = tk.Entry(self)
                self.port_entry.pack(side=tk.LEFT)
                self.baud_label = tk.Label(self, text="Baudrate:")
                self.baud_label.pack(side=tk.LEFT)
                self.baud_entry = tk.Entry(self)
                self.baud_entry.pack(side=tk.LEFT)
            def get_port(self):
                return self.port_entry.get()
            def get_baud(self):
                return self.baud_entry.get()
        self.geometry("400x300")
        self.terminal = tk.Listbox(self, bg='black', fg='white')
        self.terminal.pack(fill=tk.BOTH, expand=True)
        self.input_field = tk.Entry(self)
        self.input_field.pack(fill=tk.X)
        self.connect_button = tk.Button(self, text="Connect")
        self.connect_button.pack(fill=tk.X)
        self.details = SerialDetails(self)
        self.details.pack(fill=tk.X)
        
    def start(self):
        self.mainloop()
        
    def bind_send(self, func):
        self.input_field.bind("<Return>", func)
        
    def bind_reconnect(self, func):
        self.connect_button.config(command=func)
        
    def get_input(self):
        return self.input_field.get()
    
    def get_port(self):
        return self.details.get_port()

    def get_baud(self):
        return self.details.get_baud()
    
    def clear_input(self):
        self.input_field.delete(0, tk.END)
        
    def append_data(self, data):
        self.terminal.insert(tk.END, data)
        self.terminal.see(tk.END)  # Scroll

