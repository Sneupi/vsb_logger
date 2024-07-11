"""
File: myserial.py
Author: Gabe Venegas
Purpose: File containing classes for serial communication
"""

import datetime
import threading
import serial
import time
import queue

class SerialThread(threading.Thread):
    """Thread that allows asynchronous serial 
    send and receive. Message history is stored 
    in a queue for access by other threads.
    
    NOTE: Thread is infinite but stoppable with stop() method.
    """
    
    def __init__(self, port, baudrate):
        super().__init__()
        
        self.ser = serial.Serial(port, baudrate)
        self.txn_queue = queue.Queue()  # (TX/RX, data)
        self.running = False
        
        self.daemon = True  # threading.Thread
        
    def run(self):
        self.running = True
        while self.running:
            try:
                if self.ser.in_waiting:
                    data = self.ser.readline().decode('utf-8').strip()
                    self.txn_queue.put(('RX', data))
                else:
                    time.sleep(0.1)  # Prevent CPU hogging
            except Exception as e:
                print(f"SerialThread Error: {e}")
        self.ser.close()

    def stop(self):
        self.running = False
    
    def write(self, data: str):
        self.txn_queue.put(('TX', data.strip()))
        self.ser.write(str(data.strip() + '\n').encode('utf-8'))

    def __del__(self):
        self.stop()
         

class SerialLogger:
    """Class for logging serial RX/TX data to CSV"""
    def __init__(self, filepath, mode='a'):
        self.file = open(filepath, mode)
    
    def __format_entry(self, data, direction):
        return f'{datetime.datetime.now()},{direction},{data}\n'
    
    def __log(self, data, direction):
        if self.file.closed:
            raise Exception('Logger is closed')
        self.file.write(self.__format_entry(data, direction))
    
    def log_tx(self, data):
        self.__log(data, 'TX')
    
    def log_rx(self, data):
        self.__log(data, 'RX')
    
    def close(self):
        if self.file:
            self.file.close()
    
    def __del__(self):
        self.close()


if __name__ == "__main__":

    import tkinter as tk
    
    class SerialGUI(tk.Tk):
        """Example GUI to demonstrate 
        SerialThread and SerialLogger"""
        def __init__(self, port, baudrate, filepath):
            super().__init__()
            self.geometry("400x300")
            self.protocol("WM_DELETE_WINDOW", self.__del__)

            self.serial_logger = SerialLogger(filepath, 'w')
            self.serial_thread = SerialThread(port, baudrate)
            self.serial_thread.start()

            self.terminal = tk.Listbox(self)
            self.terminal.pack(fill=tk.BOTH, expand=True)
            self.terminal.config(bg='black', fg='white')
            
            self.input_field = tk.Entry(self)
            self.input_field.pack(fill=tk.X)
            self.input_field.bind("<Return>", self.send_data)

            self.update_transaction_history()

        def send_data(self, event):
            data = self.input_field.get()
            self.serial_thread.write(data)
            self.input_field.delete(0, tk.END)

        def update_transaction_history(self):
            """WARNING: 
            Infinitely recursive function! 
            Used as an easy scheduling hack."""
            while not self.serial_thread.txn_queue.empty():
                direction, data = self.serial_thread.txn_queue.get()
                self.serial_logger.log_tx(data) if direction == 'TX' else self.serial_logger.log_rx(data)
                self.terminal.insert(tk.END, f"{direction}: {data}")
                self.terminal.see(tk.END)  # Scroll to bottom

            self.after(100, self.update_transaction_history)

        def __del__(self):
            self.serial_thread.stop()
            self.serial_logger.close()
            self.destroy()
    
    port = "COM9"  # Replace with your serial port
    baudrate = 115200  # Replace with your desired baudrate
    filepath = "transaction_history.csv"  # Replace with your desired file path

    gui = SerialGUI(port, baudrate, filepath)
    gui.mainloop()