import tkinter as tk
import threading
import serial
import queue
import tkpanels as tkp
import datetime
import csv
import re

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style


LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

cv_data = [[] for _ in range(12)]  # 12 cells

def animate(i):
    global cv_data
    a.clear()
    a.set_title("Cell Voltage")
    a.set_xlabel("Uptime (as minutes)")
    a.set_ylabel("Raw ADC")
    for cell in range(12):
        x = [x[0] for x in cv_data[cell]]
        y = [y[1] for y in cv_data[cell]]
        a.plot(x, y, label=f"Ch{cell+1}")
    a.legend()

class SerialLogger:
    def __init__(self):
        self.logfile = None
        
    def open(self, filename):
        self.close()  # If open, close
        try:
            self.logfile = open(filename, 'a', newline='')
        except IOError as e:
            self.logfile = None
            raise e
            
    def generic_filename(self):
        """Generic filename with current datetime"""
        return f"serial_log_{datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')}.csv"
            
    def close(self):
        if self.logfile:
            self.logfile.close()
            self.logfile = None
            
    def log(self, message, is_rx):
        if self.logfile:
            writer = csv.writer(self.logfile)
            tstamp = str(datetime.datetime.now())
            writer.writerow([tstamp, 'RX' if is_rx else 'TX', message])
        else:
            raise IOError("Log file not open")

class SerialThread(threading.Thread):
    def __init__(self, serial, baud, data_queue):
        super().__init__()
        self.port = serial
        self.baud = baud
        self.data_queue = data_queue
        self.running = False
        self.ser = None
        self.logger = SerialLogger()
        
    def run(self):
        try:
            self.ser = serial.Serial(self.port, self.baud)
            self.running = True
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            return
        
        try:
            self.logger.open(self.logger.generic_filename())
        except Exception as e:
            print(e)

        while self.running:
            try:
                if self.ser.in_waiting:
                    data = self.ser.readline().decode('utf-8').strip()
                    self.__log(data, is_rx=True)
                    self.data_queue.put(data)
            except serial.SerialException as e:
                print(f"Serial read error: {e}")
                self.running = False
            except UnicodeDecodeError as e:
                print(f"Unicode error: {e}")

    def stop(self):
        self.running = False
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
            except serial.SerialException as e:
                print(f"Error closing serial port: {e}")
        self.logger.close()

    def connected(self):
        return self.ser and self.ser.is_open
    
    def write(self, data: str):
        data = data.strip() + '\n'
        ret = self.ser.write(data.encode('utf-8'))
        self.__log(data.strip(), is_rx=False)
        return ret
                
    def __log(self, message, is_rx):
        try:
            self.logger.log(message, is_rx)
        except IOError as e:
            print(e)
            
class SerialApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("App")
        self.geometry("1280x720")
        self.resizable(False, False)
        
        self.data_queue = queue.Queue()
        self.serial_thread = None

        self.setup_gui()
        self.link_controls()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.after(100, self.process_serial_data)

    def setup_gui(self):
        
        self.controls = tkp.ControlsFrame(self)
        self.controls.place(relx=0, rely=0, relwidth=0.4, relheight=0.4)
        self.controls.diag.set_led("log cpi", True)  # FIXME: logging always on
        
        self.serial_setup = tkp.SerialSetup(self)
        self.serial_setup.place(relx=0, rely=0.9, relwidth=0.4, relheight=0.1)

        self.terminal = tkp.CLIFrame(self, self.send_entry)
        self.terminal.place(relx=0, rely=0.4, relwidth=0.4, relheight=0.5)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)

    def update_controls(self, data: str):
        # FIXME: I can see this getting out 
        # of hand quickly with VSB firmware changes.
        # Also dislike how unsophistocated it is
        """Update controlpair states based on incoming data"""
        sys = self.controls.sys
        diag = self.controls.diag
        # run/stop
        if "RN:" in data:
            sys.set_led("run", True)
            sys.set_led("stop", False)
            
        elif "ST:" in data:
            sys.set_led("run", False)
            sys.set_led("stop", True)
        # balance
        elif "EB:" in data and "enabled" in data:
            sys.set_led("balance", True)
            
        elif "DB:" in data and "disabled" in data:
            sys.set_led("balance", False)
        # extbus
        elif "XE:" in data and "on" in data:
            sys.set_led("extbus", True)
            
        elif "XD:" in data and "off" in data:
            sys.set_led("extbus", False)
        # mq dump
        elif "EQ:" in data and "enabled" in data:
            sys.set_led("mq dump", True)
            
        elif "DQ:" in data and "disabled" in data:
            sys.set_led("mq dump", False)
        # cp lock  # TODO cp lock
        # debug
        elif "ED:" in data and "enabled" in data:
            diag.set_led("debug", True)
        
        elif "DD:" in data and "disabled" in data:
            diag.set_led("debug", False)
        # debug2
        elif "E2:" in data and "enabled" in data:
            diag.set_led("debug2", True)
        
        elif "D2:" in data and "disabled" in data:
            diag.set_led("debug2", False)
        # trace
        elif "TA:" in data and "active" in data:
            diag.set_led("trace", True)
        
        elif "DT:" in data and "disabled" in data:
            diag.set_led("trace", False)
        # trace2  # TODO trace2
        # info  # TODO info
        # error
        elif "EE:" in data and "enabled" in data:
            diag.set_led("error", True)
        
        elif "DE:" in data and "disabled" in data:
            diag.set_led("error", False)
        # log cpi  # TODO log cpi
        
    def append_cv_data(self, data: str):
        """If string is valid CV data, append to cv_data"""
        global cv_data
        if "DBG CV" in data:
            tstamp, ch, val = [int(_) for _ in re.findall(r'\d+', data)[-3:]]
            tstamp = tstamp / 60000  # ms to minutes
            cv_data[ch - 1].append((tstamp, val))
            
    def link_controls(self):
        # FIXME: really unsophistocated, but it works
        def _balance():
            ctrl = self.controls.sys.balance
            self.send("EB" if not ctrl.is_on else "DB")
        
        def _extbus():
            ctrl = self.controls.sys.extbus
            self.send("XE" if not ctrl.is_on else "XD")
            
        def _mq_dump():
            ctrl = self.controls.sys.mq_dump
            self.send("EQ" if not ctrl.is_on else "DQ")
            
        def _cp_lock():
            print("CP lock not implemented yet")  # TODO cp lock button
            
        def _debug():
            ctrl = self.controls.diag.debug
            self.send("ED" if not ctrl.is_on else "DD")
            
        def _debug2():
            ctrl = self.controls.diag.debug2
            self.send("E2" if not ctrl.is_on else "D2")
        
        def _trace():
            ctrl = self.controls.diag.trace
            self.send("TA" if not ctrl.is_on else "DT")

        def _trace2():
            print("Trace2 not implemented yet")  # TODO trace2 button
        
        def _info():
            print("Info not implemented yet")  # TODO; info button is vague
        
        def _error():
            ctrl = self.controls.diag.error
            self.send("EE" if not ctrl.is_on else "DE")
        
        def _log_cpi():
            print("Log CPI not implemented yet (logs currently always on)")
            # TODO: toggle CPI logging
                
        self.controls.sys.set_button_command("run", lambda: self.send("RN"))
        self.controls.sys.set_button_command("stop", lambda: self.send("ST"))
        self.controls.sys.set_button_command("balance", _balance)
        self.controls.sys.set_button_command("extbus", _extbus)
        self.controls.sys.set_button_command("mq dump", _mq_dump)
        self.controls.sys.set_button_command("cp lock", _cp_lock)
        self.controls.sys.set_button_command("connect", self.connect_serial)
        
        self.controls.diag.set_button_command("debug", _debug)
        self.controls.diag.set_button_command("debug2", _debug2)
        self.controls.diag.set_button_command("trace", _trace)
        self.controls.diag.set_button_command("trace2", _trace2)
        self.controls.diag.set_button_command("info", _info)
        self.controls.diag.set_button_command("error", _error)
        self.controls.diag.set_button_command("log cpi", _log_cpi)
        
    def connect_serial(self, event=None):
        port = self.serial_setup.get_port()
        baud_rate = self.serial_setup.get_baud()
        
        if self.serial_thread and self.serial_thread.running:
            self.serial_thread.stop()

        if port and baud_rate:
            self.serial_thread = SerialThread(port, int(baud_rate), self.data_queue)
            self.serial_thread.daemon = True
            self.serial_thread.start()
        
        self.after(250, lambda: self.controls.sys
                   .set_led("connect", self.serial_thread.running))

    def process_serial_data(self):
        while not self.data_queue.empty():
            data = self.data_queue.get()
            self.update_controls(data)
            self.append_cv_data(data)
            self.terminal.insert(data)
        self.after(100, self.process_serial_data)

    def send(self, data: str):
        if self.serial_thread and self.serial_thread.connected():
            if self.serial_thread.write(data):  # Success
                self.terminal.insert(data)
    
    def send_entry(self, event=None):
        """Sending from terminal entry"""
        data = self.terminal.get_entry()
        self.send(data)

    def on_closing(self):
        if self.serial_thread and self.serial_thread.running:
            self.serial_thread.stop()
        self.destroy()

if __name__ == "__main__":
    root = SerialApp()
    ani = animation.FuncAnimation(f, animate, interval=1000)
    root.mainloop()
