import tkinter as tk
import threading
import serial
import queue
import tkpanels as tkp
import time
import csv

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


def animate(i):
    # pullData = open("sampleText.txt","r").read()
    # dataList = pullData.split('\n')
    # xList = []
    # yList = []
    # for eachLine in dataList:
    #     if len(eachLine) > 1:
    #         x, y = eachLine.split(',')
    #         xList.append(int(x))
    #         yList.append(int(y))

    # a.clear()
    # a.plot(xList, yList)
    pass # TODO implement plot animation

class SerialThread(threading.Thread):
    def __init__(self, serial_port, baud_rate, data_queue):
        super().__init__()
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.data_queue = data_queue
        self.running = False
        self.ser = None
        self.init_timestamp = time.strftime("%Y_%m_%d_%H%M%S", time.localtime())
        self.logfile = None
        
    def run(self):
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate)
            self.running = True
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            return
        
        filename = f"serial_log_{self.init_timestamp}.csv"
        try:
            self.logfile = open(filename, 'a', newline='')
        except IOError as e:
            print(f"Error opening file: {e}")

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
        if self.logfile:
            self.logfile.close()

    def connected(self):
        return self.ser and self.ser.is_open
    
    def write(self, data: str):
        data = data.strip() + '\n'
        ret = self.ser.write(data.encode('utf-8'))
        self.__log(data.strip(), is_rx=False)
        return ret
                
    def __log(self, message, is_rx):
        if self.logfile:
            writer = csv.writer(self.logfile)
            writer.writerow(['RX' if is_rx else 'TX', message])
            
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
        
        self.serial_setup = tkp.SerialSetup(self)
        self.serial_setup.place(relx=0, rely=0.9, relwidth=0.4, relheight=0.1)

        self.terminal = tkp.CLIFrame(self, self.send_entry)
        self.terminal.place(relx=0, rely=0.4, relwidth=0.4, relheight=0.5)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)

    def link_controls(self):
        # FIXME: indiciators not necessarily 
        # reflective of device state, but of last command sent 
        
        def _run():
            self.controls.sys.set_led("run", True)
            self.controls.sys.set_led("stop", False)
            self.send("RN")
        
        def _stop():
            self.controls.sys.set_led("run", False)
            self.controls.sys.set_led("stop", True)
            self.send("ST")
        
        def _balance():
            ctrl = self.controls.sys.balance
            ctrl.toggle_led()
            self.send("EB" if ctrl.is_on else "DB")
        
        def _extbus():
            ctrl = self.controls.sys.extbus
            ctrl.toggle_led()
            self.send("XE" if ctrl.is_on else "XD")
            
        def _mq_dump():
            ctrl = self.controls.sys.mq_dump
            ctrl.toggle_led()
            self.send("EQ" if ctrl.is_on else "DQ")
            
        def _cp_lock():
            print("CP lock not implemented yet")  # TODO cp lock button
            
        def _debug():
            ctrl = self.controls.diag.debug
            ctrl.toggle_led()
            self.send("ED" if ctrl.is_on else "DD")
            
        def _debug2():
            ctrl = self.controls.diag.debug2
            ctrl.toggle_led()
            self.send("E2" if ctrl.is_on else "D2")
        
        def _trace():
            ctrl = self.controls.diag.trace
            ctrl.toggle_led()
            self.send("TA" if ctrl.is_on else "DT")

        def _trace2():
            print("Trace2 not implemented yet")  # TODO trace2 button
        
        def _info():
            print("Info not implemented yet")  # TODO; info button is vague
        
        def _error():
            ctrl = self.controls.diag.error
            ctrl.toggle_led()
            self.send("EE" if ctrl.is_on else "DE")
        
        def _log_cpi():
            print("Log CPI not implemented yet (logs currently always on)")
            # TODO: toggle CPI logging
                
        self.controls.sys.set_button_command("run", _run)
        self.controls.sys.set_button_command("stop", _stop)
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
