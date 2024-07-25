
from model import SerialModel
from .panel import PanelController
from view.view import View

class Controller:
    """VSB Controller"""
    def __init__(self, view: View):
        self.model = None
        self.view = view
        self.panel_controller = PanelController(view)  # subcontroller
        self._bind_once()
        
    def _bind_once(self):
        self.view.bind_cli_send(lambda _: self._send_data(self.view.get_cli_entry()))
        self.view.bind_connect(self._reconnect)
        self.panel_controller.clear_bindings()
        
    def _bind_each_connect(self, model: SerialModel):
        if model:
            self.panel_controller.clear_bindings()
            self.panel_controller.bind_buttons(model)
            
    def start(self):
        self.view.start()
    
    def _add_event_listeners(self, model: SerialModel):
        """Register all event listeners"""
        model.add_event_listener('rx', self.panel_controller.rx_listener)
        model.add_event_listener('rx', self._rx_listener)
        model.add_event_listener('tx', self._tx_listener)
        model.add_event_listener('connected', self._connected_listener)
        model.add_event_listener('disconnected', self._disconnected_listener)

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
            self._add_event_listeners(self.model)
            self._bind_each_connect(self.model)
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
        
        
