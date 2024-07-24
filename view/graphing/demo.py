"""
File: demos.py
Author: Gabe Venegas
Purpose: modele for package classes
"""

import matplotlib.pyplot as plt
from . import LiveGraphTk, LiveGraph
import tkinter as tk

def demo_livegraph(interval):
    import threading
    import time
    import datetime
    import random
    
    def thread_func(graph: LiveGraph):
        """Simulate graphing data coming in from a source"""
        while True:
            for i in range(12):
                t = datetime.datetime.now()
                v = random.randint(341*i, 341*(i+1))
                graph.append(f"{i}", t, v)
                time.sleep(0.07)
                
    lgf = LiveGraph(interval, width=datetime.timedelta(seconds=10))
    
    thread = threading.Thread(target=thread_func, args=(lgf,))
    thread.daemon = True
    thread.start()
    
    plt.show()
    
    print("DEMO END")
    
def demo_livegraph_tk(interval):
    import threading
    import time
    import random
    
    def thread_func(graph: LiveGraphTk):
        """Simulate graphing data coming in from a source"""
        while True:
            for i in range(12):
                v = random.randint(341*i, 341*(i+1))
                graph.append(f"{i}", v)
                time.sleep(0.07)
    
    root = tk.Tk()
    gph = LiveGraphTk(root, interval)
    gph.pack(fill=tk.BOTH, expand=True)
                
    thread = threading.Thread(target=thread_func, args=(gph,))
    thread.daemon = True
    thread.start()
    
    # FIXME tkinter not exiting mainloop after close unless
    # root.protocol("WM_DELETE_WINDOW", lambda: root.quit() or root.destroy())  
    root.mainloop()
