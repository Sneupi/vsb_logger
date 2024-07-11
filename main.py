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
        
        def send(if_false: str, if_true: str, led_name: str):
            """Send if_true if LED is off, else if_false"""
            self.write(if_true if self.gui.get_led(led_name) else if_false)
                
        self.gui.bind_button("run", lambda: send("RN", "ST", "run"))
        self.gui.bind_button("stop", lambda: send("ST", "RN", "stop"))
        self.gui.bind_button("balance", lambda: send("EB", "DB", "balance"))
        self.gui.bind_button("extbus", lambda: send("XE", "XD", "extbus"))
        self.gui.bind_button("mq dump", lambda: send("EQ", "DQ", "mq dump"))
        self.gui.bind_button("show dn", lambda: send("SN", "", "show dn"))
        
        self.gui.bind_button("debug", lambda: send("ED", "DD", "debug"))
        self.gui.bind_button("debug2", lambda: send("E2", "D2", "debug2"))
        self.gui.bind_button("trace", lambda: send("TA", "DT", "trace"))
        self.gui.bind_button("trace2", lambda: print("Trace2 not implemented yet"))  # TODO trace2 button
        self.gui.bind_button("info", lambda: send("SH", "", "info"))  # FIXME info button vague; SH for now 
        self.gui.bind_button("error", lambda: send("EE", "DE", "error"))
        
        
    def run(self):
        """Serial read loop for updating app"""
        self.running = True
        while self.running:
            try:
                while self.ser and self.ser.is_open and self.ser.in_waiting:
                    data = self.ser.readline().decode('utf-8').strip()
                    self.gui.update_terminal(data)
                    # TODO (if ctrl_status) update buttons
                    # TODO (if stats) update stats
                    # TODO (if cv_data) update graph
                    if self.gui.filebrowser.enabled:
                        self.logger.log_rx(data)
                else:
                    time.sleep(0.01)  # Prevent CPU hogging
            except OSError as e:
                pass  # Serial port closed
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