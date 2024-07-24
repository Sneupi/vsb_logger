import threading
import queue
import serial
import time
from .base import ObservableModel


class SerialThread(threading.Thread):
    """Thread that allows asynchronous send and 
    synchronous (code-blocking) receive.
    """
    
    def __init__(self, port, baudrate, model: 'SerialModel'):
        super().__init__()
        self.model = model
        self.tx_q = queue.Queue()
        self.daemon = True  # threading.Thread
        self.ser = serial.Serial(port, baudrate)
    
    def __get_rx(self):
        try:
            if self.ser.in_waiting > 0:
                data = self.ser.readline().decode('utf-8').strip()
                self.model.last_rx = data
                self.model.trigger_event('rx')
                return True
        except OSError as e:
            pass  # related to in_waiting after serial close
        except UnicodeDecodeError as e:
            e.reason = "(likely baud mismatch) " + e.reason
            print(f"SerialThread Error: {e}")
        return False
    
    def __get_tx(self):
        try:
            if not self.tx_q.empty():
                data = self.tx_q.get()
                self.ser.write(str(data).encode('utf-8'))
                self.model.last_tx = data
                self.model.trigger_event('tx')
                return True
        except serial.SerialException as e:
            print(f"SerialThread Error: {e}")
        return False
    
    def run(self):
        while self.ser.is_open:
            t = self.__get_tx()
            r = self.__get_rx()
            if not t and not r:
                time.sleep(0.02)
            
        print("done")
        
    def write(self, data: str):
        self.tx_q.put(data)
        
    def stop(self):
        if self.is_alive():
            self.ser.close()
        
    def __del__(self):
        self.stop()
         
class SerialModel(ObservableModel):
    """ObservableModel for serial send and receive.
    NOTE: Code-blocking on RX to call registered listener functions
    """
    
    def __init__(self, port, baudrate):
        super().__init__()
        self._thread = SerialThread(port, baudrate, self)
        self.last_rx = None
        self.last_tx = None
        self.trigger_event('connected')
        
    def write(self, data: str):
        self._thread.write(data)
        
    def start(self):
        self._thread.start()
        
    def stop(self):
        self._thread.stop()
