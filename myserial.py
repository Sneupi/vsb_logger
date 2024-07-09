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
    def __init__(self, filepath):
        self.file = open(filepath, 'a')
    
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
        self.file.close()
    
    def __del__(self):
        self.close()