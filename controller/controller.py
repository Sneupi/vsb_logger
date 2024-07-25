import tkinter as tk
from model import SerialModel
from .panel import PanelController
from .view import TestView
    
class Controller:
    """Controller for connection between 
    Model and View of VSB app"""
    pass
        
    
class TestController:
    """Example controller to demonstrate 
    SerialModel and SerialThread"""
    def __init__(self, view: TestView):
        self.model = None
        self.view = view
        self.panel_controller = PanelController(view)  # subcontroller
        
        self.view.bind_cli_send(lambda _: self._send_data(self.view.get_cli_entry()))
        self.view.bind_connect(self._reconnect)
        
    def start(self):
        self.view.start()
    
    def _add_event_listeners(self):
        if not self.model:
            return
        self.model.add_event_listener('rx', self.panel_controller.rx_listener)
        self.model.add_event_listener('rx', self._rx_listener)
        self.model.add_event_listener('tx', self._tx_listener)
        self.model.add_event_listener('connected', self._connected_listener)
        self.model.add_event_listener('disconnected', self._disconnected_listener)

    def _send_data(self, data: str):
        if self.model:
            self.model.write(data.strip() + '\n')
            
    def _reconnect(self):
        if self.model:
            self.model.stop()
        try:
            port = self.view.get_port()
            baud = self.view.get_baud()
            self.model = SerialModel(port, int(baud))
            self.panel_controller.clear_bindings()
            self.panel_controller.bind_buttons(self.model)
            self._add_event_listeners()
            self.model.start()
        except Exception as e:
            print(f"SerialController Error: {e}")
            
    def _rx_listener(self, model: SerialModel):
        self.view.append_cli(str(model.last_rx).strip())
        
    def _tx_listener(self, model: SerialModel):
        self.view.append_cli(str(model.last_tx).strip())
        
    def _connected_listener(self, model: SerialModel):
        self.view.set_connected(True)
        
    def _disconnected_listener(self, model: SerialModel):
        self.view.set_connected(False)
        
        
