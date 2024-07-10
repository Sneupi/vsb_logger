"""
File: main.py
Author: Gabe Venegas
Purpose: File joining components for VSB logger
"""

import threading

class VSBApp(threading.Thread):
    """Controller thread for managing serial, logging, and GUI 
    components of the VSB logger and plotter.
    
    NOTE: Thread is infinite but stoppable with stop() method.
    """