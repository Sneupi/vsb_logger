import tkinter as tk
from tkinter import ttk
import threading
import serial
import queue

class SerialSetup(tk.Frame):
    """User interface for setting up serial connection"""
    def __init__(self, parent, connect_func):
        super().__init__(parent)
        self.port_label = tk.Label(parent, text="Serial Port:")
        self.port_label.pack(padx=10, pady=5)

        self.port_entry = tk.Entry(parent)
        self.port_entry.pack(padx=10, pady=5)

        self.baud_label = tk.Label(parent, text="Baud Rate:")
        self.baud_label.pack(padx=10, pady=5)

        self.baud_entry = tk.Entry(parent)
        self.baud_entry.pack(padx=10, pady=5)

        self.connect_button = tk.Button(parent, text="Connect", command=connect_func)
        self.connect_button.bind('<Return>', connect_func)
        self.connect_button.pack(padx=10, pady=5)
    
    def get_port(self):
        return self.port_entry.get()
    def get_baud(self):
        return self.baud_entry.get()

class SerialThread(threading.Thread):
    def __init__(self, serial_port, baud_rate, data_queue):
        super().__init__()
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.data_queue = data_queue
        self.running = False
        self.ser = None

    def run(self):
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate)
            self.running = True
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            return

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

class SerialApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("App")

        self.data_queue = queue.Queue()
        self.serial_thread = None

        self.setup_gui()
        self.root.after(100, self.process_serial_data)

    def setup_gui(self):
        
        self.serial_setup = SerialSetup(self.root, self.connect_serial)
        self.serial_setup.pack(padx=10, pady=10)

        self.terminal = tk.Text(self.root, state='disabled', width=80, height=20)
        self.terminal.pack(padx=10, pady=10)

        self.send_entry = tk.Entry(self.root)
        self.send_entry.bind('<Return>', self.send_data)
        self.send_entry.pack(padx=10, pady=10)

    def connect_serial(self, event=None):
        port = self.serial_setup.get_port()
        baud_rate = self.serial_setup.get_baud()
        
        if self.serial_thread and self.serial_thread.running:
            self.serial_thread.stop()

        if port and baud_rate:
            self.serial_thread = SerialThread(port, int(baud_rate), self.data_queue)
            self.serial_thread.daemon = True
            self.serial_thread.start()

    def process_serial_data(self):
        while not self.data_queue.empty():
            data = self.data_queue.get()
            self.log_message(data)
        self.root.after(100, self.process_serial_data)

    def send_data(self, event=None):
        data = self.send_entry.get()
        self.send_entry.delete(0, 'end')
        if self.serial_thread and self.serial_thread.ser and self.serial_thread.ser.is_open:
            try:
                self.serial_thread.ser.write(data.encode('utf-8'))
                self.log_message(data)
            except serial.SerialException as e:
                print(f"Serial write error: {e}")

    def log_message(self, message):
        self.terminal.config(state='normal')
        self.terminal.insert('end', message + '\n')
        self.terminal.config(state='disabled')
        self.terminal.see('end')

    def on_closing(self):
        if self.serial_thread and self.serial_thread.running:
            self.serial_thread.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
