
import threading
import time

class ProbeThread(threading.Thread):
    """Stoppable thread for probing stats every N seconds"""
    def __init__(self, model, sec_freq):
        super().__init__()
        self.model = model
        self.sec_freq = sec_freq
        self.running = False
        self.daemon = True
        
    def run(self):
        print("ProbeThread: Running")
        self.running = True
        while self.running:
            self.model.write("SS\n")  # FIXME hardcoded
            time.sleep(self.sec_freq)
        print("ProbeThread: Stopped")
            
    def stop(self):
        self.running = False
        del self
        
    def __del__(self):
        self.stop()
