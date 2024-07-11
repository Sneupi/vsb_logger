"""
File: main.py
Author: Gabe Venegas
Purpose: File joining components for VSB logger
"""

import threading
import serial
import time
from tkpanels import VSBGUI
from myserial import SerialLogger
import re

class VSBApp(threading.Thread):
    """Controller thread for managing serial, logging, and GUI 
    components of the VSB logger and plotter.
    
    NOTE: Thread is infinite but stoppable with stop() method.
    """
    
    def __init__(self, gui: VSBGUI):
        super().__init__()
        
        self.running = False
        self.gui = gui
        self.ser = None
        self.logger = None
        
        self.daemon = True  # threading.Thread
        self.bind_functions()
        
    def bind_functions(self):
        """Bind functionality to GUI elements"""
        self.gui.call_on_exit(self.stop)
            
        self.gui.bind_button("connect", self.connect_serial)
        self.gui.bind_button("log cpi", self.toggle_logger)
        self.gui.bind_terminal_send(lambda _: self.write(self.gui.terminal.get_entry()))
        self.gui.bind_button("clear err", lambda: self.write("ER"))  # FIXME maybe not "ER"
        
        def send(if_false: str, if_true: str, led_name: str):
            """Send if_true if LED is off, else if_false"""
            self.write(if_true if self.gui.get_led(led_name) else if_false)
                
        self.gui.bind_button("run", lambda: send("RN", "ST", "run"))
        self.gui.bind_button("stop", lambda: send("ST", "RN", "stop"))
        self.gui.bind_button("balance", lambda: send("EB", "DB", "balance"))
        self.gui.bind_button("extbus", lambda: send("XE", "XD", "extbus"))
        self.gui.bind_button("mq dump", lambda: send("EQ", "DQ", "mq dump"))
        self.gui.bind_button("show dn", lambda: self.write("SN"))
        
        self.gui.bind_button("debug", lambda: send("ED", "DD", "debug"))
        self.gui.bind_button("debug2", lambda: send("E2", "D2", "debug2"))
        self.gui.bind_button("trace", lambda: send("TA", "DT", "trace"))
        self.gui.bind_button("trace2", lambda: print("Trace2 not implemented yet"))  # TODO trace2 button
        self.gui.bind_button("info", lambda: send("SH", "", "info"))  # FIXME info button vague; SH for now 
        self.gui.bind_button("error", lambda: send("EE", "DE", "error"))
        
    def gui_update_buttons(self, data: str):
        """Update GUI buttons based on incoming data strings"""
        # FIXME hardcoded strings
        
        # run/stop
        if "RN:" in data:
            self.gui.update_button("run", True)
            self.gui.update_button("stop", False)
            
        elif "ST:" in data:
            self.gui.update_button("run", False)
            self.gui.update_button("stop", True)
        # balance
        elif "EB:" in data and "enabled" in data:
            self.gui.update_button("balance", True)
            
        elif "DB:" in data and "disabled" in data:
            self.gui.update_button("balance", False)
        # extbus
        elif "XE:" in data and "on" in data:
            self.gui.update_button("extbus", True)
            
        elif "XD:" in data and "off" in data:
            self.gui.update_button("extbus", False)
        # mq dump
        elif "EQ:" in data and "enabled" in data:
            self.gui.update_button("mq dump", True)
            
        elif "DQ:" in data and "disabled" in data:
            self.gui.update_button("mq dump", False)
        # show dn
        elif "SN:" in data and "-> ON" in data:
            self.gui.update_button("show dn", True)
        elif "SN:" in data and "-> OFF" in data:
            self.gui.update_button("show dn", False)
        # debug
        elif "ED:" in data and "enabled" in data:
            self.gui.update_button("debug", True)
        
        elif "DD:" in data and "disabled" in data:
            self.gui.update_button("debug", False)
        # debug2
        elif "E2:" in data and "enabled" in data:
            self.gui.update_button("debug2", True)
        
        elif "D2:" in data and "disabled" in data:
            self.gui.update_button("debug2", False)
        # trace
        elif "TA:" in data and "active" in data:
            self.gui.update_button("trace", True)
        
        elif "DT:" in data and "disabled" in data:
            self.gui.update_button("trace", False)
        # trace2  # TODO trace2
        # info
        elif data == "AD n         Immediate ADC DAQ from channel n":
            self.gui.update_button("info", True)
        elif data == "XE           Enable extension bus":
            self.gui.update_button("info", False)
        # error
        elif "EE:" in data and "enabled" in data:
            self.gui.update_button("error", True)
        
        elif "DE:" in data and "disabled" in data:
            self.gui.update_button("error", False)
        
    def gui_update_stats(self, data: str):
        """Update GUI stats based on incoming data strings"""
        # FIXME hardcoded strings
        try:
            status = data.split(":")[-1].strip()
        except Exception:
            return
        
        if   "PVM state :" in data:
            self.gui.update_statistic("pvm", status)
        elif "CTC state :" in data:
            self.gui.update_statistic("ctc", status)
        elif "Last CV   :" in data:
            self.gui.update_statistic("last cv", status)
        elif "Last CV DN:" in data:
            self.gui.update_statistic("last cv dn", status)
        elif "Err count :" in data:
            self.gui.update_statistic("errs", status)
        elif "Last Error:" in data:
            self.gui.update_statistic("last err", status)
            
    def gui_update_graph(self, data: str):
        """Update GUI graph based on incoming data strings"""
        # FIXME hardcoded strings
        if "DBG CV" in data:
            x, ch, y = [int(num) for num in re.findall(r'\d+', data)][-3:]
            self.gui.update_graph(ch, x, y)
        
    def run(self):
        """Serial read loop for updating app"""
        
        def probe_stats(app, sec_freq):
            """Probe stats every N seconds infinitely"""
            while True:
                app.write("SS")
                time.sleep(sec_freq)
        timer_thread = threading.Thread(target=probe_stats, args=(self, 4))
        timer_thread.daemon = True
        timer_thread.start()
        
        self.running = True
        while self.running:
            try:
                while self.ser and self.ser.is_open and self.ser.in_waiting:
                    data = self.ser.readline().decode('utf-8').strip()
                    self.gui.update_terminal(data)
                    self.gui_update_buttons(data)
                    self.gui_update_stats(data)
                    self.gui_update_graph(data)
                    if self.gui.filebrowser.enabled:
                        self.logger.log_rx(data)
                else:
                    time.sleep(0.01)  # Prevent CPU hogging
            except OSError as e:
                pass  # FIXME workaround, avoid err spam on changed serial
            except Exception as e:
                self.print_error(e)
                
        if self.ser:
            self.ser.close()
        self.destroy_logger()
            
    def stop(self):
        self.running = False
        
    def print_error(self, msg: str):
        print(f"VSBApp Error: {msg}")
    
    def write(self, data: str):
        """Serial write method which also 
        updates GUI terminal (and log)"""
        if self.ser and self.ser.is_open:
            self.ser.write(str(data.strip() + '\n').encode('utf-8'))
            self.gui.update_terminal(data)
            if self.gui.filebrowser.enabled:
                self.logger.log_tx(data)
        else: 
            self.print_error(f"Serial not open; cannot write \"{data}\"")
    
    def connect_serial(self, port, baudrate):
        """Return True if successful, else False"""
        if self.ser:
            self.ser.close()
        try:
            self.ser = serial.Serial(port, baudrate)
            return True
        except Exception as e:
            self.print_error(e)
            return False
            
    def destroy_logger(self):
        """Close logger file"""
        if self.logger:
            self.logger.close()

    def toggle_logger(self):
        """Toggle logger create/destroy
        
        Returns True if logger is created, 
        False if destroyed or failure."""
        if self.gui.filebrowser.enabled:
            self.destroy_logger()
            return False
        else:
            try:
                self.logger = SerialLogger(self.gui.filebrowser.get_path())
                return True
            except Exception as e:
                self.print_error(e)
                return False
        
    def __del__(self):
        self.stop()

if __name__ == '__main__':
    gui = VSBGUI()
    app = VSBApp(gui)
    app.start()
    gui.mainloop()