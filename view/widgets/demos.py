
import tkinter as tk
from .status_box import StatusBox
from .widget_grid import LEDGrid, StatusGrid
from .led_button import LEDButton
from .file_action import FileAction
from .serial_connector import SerialConnector
from .cli import CLI
from .live_graph_tk import LiveGraphTk

def demo_cli():
    root = tk.Tk()
    cli = CLI(root)
    cli.pack(expand=True, fill='both')
    def recursive_counter(n=0):
        cli.insert(f"{n} seconds have passed")
        root.after(1000, recursive_counter, n+1)
    def example_send_func(event):
        cli.insert(cli.get_entry())
    cli.set_send_func(example_send_func)
    recursive_counter()
    root.mainloop()

def demo_status_frame_grid():
    root = tk.Tk()
    grid = StatusGrid(root, [["Voltage", "Current", "Power"], ["Temp", "Humidity", "Pressure"]])
    grid.pack(expand=True, fill='both')
    def recursive_counter(n=0):
        for i, name in enumerate(grid.get_names()):
            grid.set_readout(name, f"num {n+i}")
        root.after(1000, recursive_counter, n+1)
    recursive_counter()
    root.mainloop()
    
def demo_led_button_grid():
    root = tk.Tk()
    grid = LEDGrid(root, [["LED1", "LED2", "LED3"], ["LED4", "LED5", "LED6"]])
    grid.pack(expand=True, fill='both')
    
    grid.set_command("LED1", lambda: grid.set_led("LED1", not grid.get_led("LED1")))
    grid.set_command("LED2", lambda: grid.set_led("LED2", not grid.get_led("LED2")))
    grid.set_command("LED3", lambda: grid.set_led("LED3", not grid.get_led("LED3")))
    grid.set_command("LED4", lambda: grid.set_led("LED4", not grid.get_led("LED4")))
    grid.set_command("LED5", lambda: grid.set_led("LED5", not grid.get_led("LED5")))
    grid.set_command("LED6", lambda: grid.set_led("LED6", not grid.get_led("LED6")))
        
    root.mainloop()
    
def demo_status_frame():
    root = tk.Tk()
    frame = StatusBox(root, "TestString")
    frame.pack(expand=True, fill='both')
    def recursive_counter(n=0):
        frame.set_readout(f"num {n}")
        root.after(1000, recursive_counter, n+1)
    recursive_counter()
    root.mainloop()
    
def demo_led_button():
    root = tk.Tk()
    led_button = LEDButton(root, text="TestString")
    led_button.pack(expand=True, fill='both')
    def test_command():
        led_button.set_led(not led_button.get_led())
        print(f"Test Toggled LED: {led_button.get_led()}")
    led_button.set_command(test_command)
    root.mainloop()
    
def demo_file_action():
    root = tk.Tk()
    file_action = FileAction(root, text="SomeAction")
    file_action.pack(expand=True, fill='both')
    def test_command():
        fp = file_action.get_path()
        print(f"Test Command, ON if nonempty path: {fp}")
        file_action.set_button_state(fp != "")
    file_action.set_command(test_command)
    root.mainloop()
    
def demo_serial_connector():
    root = tk.Tk()
    serial_connector = SerialConnector(root)
    serial_connector.pack(expand=True, fill='both')
    serial_connector.set_connect_func(lambda: 
        print(f"{serial_connector.get_port()} and {serial_connector.get_baud()}"))
    root.mainloop()

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
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit() or root.destroy())  
    root.mainloop()

def demo_all():
    demo_status_frame_grid()
    demo_led_button_grid()
    demo_status_frame()
    demo_led_button()
    demo_file_action()
    demo_serial_connector()
    demo_cli()
    demo_livegraph_tk(500)