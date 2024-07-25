
import datetime

class SerialLogger:
    """Class for logging serial RX/TX data to file"""
    def __init__(self, filepath, mode='a'):
        if not filepath or filepath == '':
            raise OSError("SerialLogger null path: {}".format(filepath))
        elif not filepath.endswith(('.csv', '.txt')):
            raise OSError("SerialLogger invalid file extension: {}".format(filepath))
        else:
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
        try:
            if self.file:
                self.file.close()
        except Exception:
            pass  # File already closed
    
    def __del__(self):
        self.close()