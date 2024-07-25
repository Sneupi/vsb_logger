from model import SerialModel
from view.view import View

class PanelController:
    """Specifically for VSB button panel"""
    def __init__(self, view: View):
        self.view = view.controls
        
    def bind_buttons(self, model: SerialModel):
        def send(led_name: str, if_true: str, if_false: str):
            """Send if_true if LED is off, else if_false"""
            model.write(if_true+'\n' if self.view.get_led(led_name) else if_false+'\n')
        def set_sender(led_name: str, if_false: str, if_true: str):
            self.view.set_button_command(led_name, lambda: send(led_name, if_false, if_true))
            
        set_sender("Run", "ST", "RN")
        set_sender("Stop", "RN", "ST")
        set_sender("Balance", "DB", "EB")
        set_sender("ExtBus", "XD", "XE")
        set_sender("MQ Dump", "DQ", "EQ")
        set_sender("Show DN", "SN", "SN")
        set_sender("Debug", "DD", "ED")
        set_sender("Debug2", "D2", "E2")
        set_sender("Trace", "DT", "TA")
        # set_button("Trace2", "D2", "E2")  #TODO
        set_sender("Info", "", "SH")
        set_sender("Error", "DE", "EE")
        
    def clear_bindings(self):
        self.view.set_button_command("Run", lambda: None)
        self.view.set_button_command("Stop", lambda: None)
        self.view.set_button_command("Balance", lambda: None)
        self.view.set_button_command("ExtBus", lambda: None)
        self.view.set_button_command("MQ Dump", lambda: None)
        self.view.set_button_command("Show DN", lambda: None)
        self.view.set_button_command("Debug", lambda: None)
        self.view.set_button_command("Debug2", lambda: None)
        self.view.set_button_command("Trace", lambda: None)
        self.view.set_button_command("Trace2", lambda: None)
        self.view.set_button_command("Info", lambda: None)
        self.view.set_button_command("Error", lambda: None)
        
    def rx_listener(self, model: SerialModel):
        self._run_listener(model)
        self._stop_listener(model)
        self._balance_listener(model)
        self._extbus_listener(model)
        self._mq_dump_listener(model)
        self._show_dn_listener(model)
        self._debug_listener(model)
        self._debug2_listener(model)
        self._trace_listener(model)
        self._trace2_listener(model)
        self._info_listener(model)
        self._error_listener(model)
    
    def _run_listener(self, model: SerialModel):
        if "RN:" in model.last_rx:
            self.view.set_led("Run", True)
            self.view.set_led("Stop", False)
            
    def _stop_listener(self, model: SerialModel):
        if "ST:" in model.last_rx:
            self.view.set_led("Run", False)
            self.view.set_led("Stop", True)
    
    def _balance_listener(self, model: SerialModel):
        d = model.last_rx
        if "EB:" in d and "enabled" in d:
            self.view.set_led("Balance", True)
        elif "DB:" in d and "disabled" in d:
            self.view.set_led("Balance", False)
            
    def _extbus_listener(self, model: SerialModel):
        d = model.last_rx
        if "XE:" in d and "on" in d:
            self.view.set_led("ExtBus", True)
        elif "XD:" in d and "off" in d:
            self.view.set_led("ExtBus", False)
            
    def _mq_dump_listener(self, model: SerialModel):
        d = model.last_rx
        if "EQ:" in d and "enabled" in d:
            self.view.set_led("MQ Dump", True)
        elif "DQ:" in d and "disabled" in d:
            self.view.set_led("MQ Dump", False)
            
    def _show_dn_listener(self, model: SerialModel):
        d = model.last_rx
        if "SN:" in d and "-> ON" in d:
            self.view.set_led("Show DN", True)
        elif "SN:" in d and "-> OFF" in d:
            self.view.set_led("Show DN", False)
            
    def _debug_listener(self, model: SerialModel):
        d = model.last_rx
        if "ED:" in d and "enabled" in d:
            self.view.set_led("Debug", True)
        elif "DD:" in d and "disabled" in d:
            self.view.set_led("Debug", False)
    
    def _debug2_listener(self, model: SerialModel):
        d = model.last_rx
        if "E2:" in d and "enabled" in d:
            self.view.set_led("Debug2", True)
        elif "D2:" in d and "disabled" in d:
            self.view.set_led("Debug2", False)
    
    def _trace_listener(self, model: SerialModel):
        d = model.last_rx
        if "TA:" in d and "active" in d:
            self.view.set_led("Trace", True)
        elif "DT:" in d and "disabled" in d:
            self.view.set_led("Trace", False)
    
    def _trace2_listener(self, model: SerialModel):
        pass # TODO
    
    def _info_listener(self, model: SerialModel):
        data = model.last_rx
        if data == "AD n         Immediate ADC DAQ from channel n":
            self.view.set_led("Info", True)
        elif data == "XE           Enable extension bus":
            self.view.set_led("Info", False)
            
    def _error_listener(self, model: SerialModel):
        d = model.last_rx
        if "EE:" in d and "enabled" in d:
            self.view.set_led("Error", True)
        elif "DE:" in d and "disabled" in d:
            self.view.set_led("Error", False)
    