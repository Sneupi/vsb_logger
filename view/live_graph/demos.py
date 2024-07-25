"""
File: demos.py
Author: Gabe Venegas
Purpose: modele for package classes
"""

from .live_graph import LiveGraph

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
                
    lgf = LiveGraph(interval=interval, width=datetime.timedelta(seconds=10))
    
    thread = threading.Thread(target=thread_func, args=(lgf,))
    thread.daemon = True
    thread.start()
    
    lgf.show()
    
    print("DEMO END")