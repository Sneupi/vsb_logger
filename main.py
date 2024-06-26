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
    pass # TODO

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
        
        # TODO tweak plot
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)

    def link_controls(self):
        # TODO replace all "AA" placeholders
        self.controls.sys.set_button_command("run", lambda: self.send("RN"))
        self.controls.sys.set_button_command("stop", lambda: self.send("ST"))
        self.controls.sys.set_button_command("balance", lambda: self.send("AA"))  # TODO
        self.controls.sys.set_button_command("extbus", lambda: self.send("AA"))  # TODO
        self.controls.sys.set_button_command("mq dump", lambda: self.send("AA"))  # TODO
        self.controls.sys.set_button_command("cp lock", lambda: self.send("AA"))  # TODO
        self.controls.sys.set_button_command("connect", self.connect_serial)
        
        self.controls.diag.set_button_command("debug", lambda: self.send("AA"))
        self.controls.diag.set_button_command("debug2", lambda: self.send("AA"))
        self.controls.diag.set_button_command("trace", lambda: self.send("AA"))
        self.controls.diag.set_button_command("trace2", lambda: self.send("AA"))
        self.controls.diag.set_button_command("info", lambda: self.send("AA"))
        self.controls.diag.set_button_command("error", lambda: self.send("AA"))
        self.controls.diag.set_button_command("log cpi", lambda: self.send("AA"))
        
    def connect_serial(self, event=None):
        port = self.serial_setup.get_port()
        baud_rate = self.serial_setup.get_baud()
        
        if self.serial_thread and self.serial_thread.running:
            self.serial_thread.stop()
            
        self.controls.sys.set_led("connect", False) 
        
        if port and baud_rate:
            self.serial_thread = SerialThread(port, int(baud_rate), self.data_queue)
            self.serial_thread.daemon = True
            self.serial_thread.start()
        
        self.after(250, lambda: self.controls.sys.set_led("connect", True) 
                            if self.serial_thread.running else None)

    def process_serial_data(self):
        while not self.data_queue.empty():
            data = self.data_queue.get()
            self.log_message(data, True)
            self.terminal.insert(data)
        self.after(100, self.process_serial_data)

    def send(self, data):
        data = data.strip() + '\n'
        if self.serial_thread and self.serial_thread.ser and self.serial_thread.ser.is_open:
            try:
                self.serial_thread.ser.write(data.encode('utf-8'))
                self.log_message(data.strip(), False)
                self.terminal.insert(data)
            except serial.SerialException as e:
                print(f"Serial write error: {e}")
    
    def send_entry(self, event=None):
        """Sending from terminal entry"""
        data = self.terminal.get_entry()
        self.send(data)
        

    def log_message(self, message, is_rx):
        if self.serial_thread and self.serial_thread.logfile:
            writer = csv.writer(self.serial_thread.logfile)
            writer.writerow(['RX' if is_rx else 'TX', message])

    def on_closing(self):
        if self.serial_thread and self.serial_thread.running:
            self.serial_thread.stop()
        self.destroy()

if __name__ == "__main__":
    root = SerialApp()
    ani = animation.FuncAnimation(f, animate, interval=1000)
    root.mainloop()
