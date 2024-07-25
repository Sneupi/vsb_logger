
from model.main import Model
from .panel import PanelController
from view.main import View
from logger import SerialLogger
from .probe import ProbeThread
import re

class Controller:
    """VSB Controller"""
    def __init__(self, view: View):
        self.model = None
        self.view = view
        self.panel_controller = PanelController(view)  # subcontroller
        
        self.probe_thread = None
        self.logger = None
        self.generic_regex = False
        
        self._bind_once()
    
    def _bind_once(self):
        self.view.bind_mode_button(self._toggle_generic_regex)
        self.view.bind_cli_send(lambda _: self._send_data(self.view.get_cli_entry()))
        self.view.bind_connect(self._reconnect)
        self.view.bind_log(self._toggle_logging)
        self.panel_controller.clear_bindings()
        
    def _bind_each_connect(self, model: Model):
        if model:
            self.panel_controller.clear_bindings()
            self.panel_controller.bind_buttons(model)
            
    def start(self):
        self.view.start()
    
    def _add_event_listeners(self, model: Model):
        """Register all event listeners"""
        model.add_event_listener('rx', self._rx_listener)
        model.add_event_listener('tx', self._tx_listener)
        model.add_event_listener('connected', self._connected_listener)
        model.add_event_listener('disconnected', self._disconnected_listener)

    def _toggle_generic_regex(self):
        self.generic_regex = not self.generic_regex
        self.view.set_mode(self.generic_regex)
        
    def _toggle_logging(self):
        if self.logger:
            self.logger.close()
            self.logger = None
        else:
            path = str(self.view.log.get_path())
            if not path.endswith(('.csv', '.txt')):
                print(f"Invalid log extension: {path}. Must be .csv or .txt")
                return
            self.logger = SerialLogger(path)
        self.view.log.set_button_state(self.logger is not None)
    
    def _start_probe(self, model):
        """Probe thread to fetch statistics periodically"""
        if not self.probe_thread:
            self.probe_thread = ProbeThread(model, 2)
            self.probe_thread.start()
            
    def _stop_probe(self):
        if self.probe_thread:
            self.probe_thread.stop()
            self.probe_thread = None
    
    def _send_data(self, data: str):
        if self.model:
            self.model.write(data.strip() + '\n')
            
    def _reconnect(self):
        if self.model:
            self._stop_probe()
            self.model.stop()
        try:
            port = self.view.get_port()
            baud = self.view.get_baud()
            self.model = Model(port, int(baud))
            self._add_event_listeners(self.model)
            self._bind_each_connect(self.model)
            self._start_probe(self.model)
            self.model.start()
        except Exception as e:
            print(f"SerialController Error: {e}")
    
    def _stat_listener(self, model: Model):
        """RX listener on probed statistics"""
        if "PVM state :" in model.last_rx:
            self.view.set_readout("PVM", model.last_rx.split(':')[-1])
        elif "CTC state :" in model.last_rx:
            self.view.set_readout("CTC", model.last_rx.split(':')[-1])
        elif "Last CV   :" in model.last_rx:
            self.view.set_readout("Last CV", model.last_rx.split(':')[-1])
        elif "Last CV DN:" in model.last_rx:
            self.view.set_readout("Last CV DN", model.last_rx.split(':')[-1])
        elif "Err count :" in model.last_rx:
            self.view.set_readout("Errs", model.last_rx.split(':')[-1])
        elif "Last Error:" in model.last_rx:
            self.view.set_readout("Last Err", model.last_rx.split(':')[-1])

    def _graphing_listener(self, model: Model):
        """RX listener"""
        if re.search(r"\d+:\s+\d+", model.last_rx):
            # FIXME hardcoded "DBG CV"
            if (not self.generic_regex and "DBG CV" in model.last_rx) or self.generic_regex:
                channel, val = re.findall(r"\d+", model.last_rx)[-2:]
                self.view.append_graph(int(channel), int(val))
    
    def _rx_listener(self, model: Model):
        self.view.append_cli(model.last_rx)
        if self.logger:
            self.logger.log_rx(model.last_rx)
        self.panel_controller.rx_listener(model)
        self._graphing_listener(model)
        self._stat_listener(model)
        
    def _tx_listener(self, model: Model):
        self.view.append_cli(model.last_tx)
        if self.logger:
            self.logger.log_tx(model.last_tx)
            
    def _connected_listener(self, model: Model):
        self.view.set_connected(True)
        
    def _disconnected_listener(self, model: Model):
        self.view.set_connected(False)
        
        
