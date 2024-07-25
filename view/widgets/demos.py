
import tkinter as tk
from .status_frame import StatusFrame
from .widget_grid import WidgetGrid
from .led_button import LEDButton
from .file_action import FileAction
from .serial_connector import SerialConnectorFrame

def demo_status_frame_grid():
    root = tk.Tk()
    grid = WidgetGrid(root, StatusFrame, [["Voltage", "Current", "Power"], ["Temp", "Humidity", "Pressure"]])
    grid.pack(expand=True, fill='both')
    def recursive_counter(n=0):
        for i, value in enumerate(grid.get_widgets().values()):
            value.set_readout(f"num {n+i}")
        root.after(1000, recursive_counter, n+1)
    recursive_counter()
    root.mainloop()
    
def demo_led_button_grid():
    root = tk.Tk()
    grid = WidgetGrid(root, LEDButton, [["LED1", "LED2", "LED3"], ["LED4", "LED5", "LED6"]])
    grid.pack(expand=True, fill='both')
    keys = [f"LED{i}" for i in range(1, 7)]
    for key in keys:
        grid.get_widgets()[key].set_command(lambda: print(f"Command for {key}"))  # FIXME not working as intended
        
    root.mainloop()
    
def demo_status_frame():
    root = tk.Tk()
    frame = StatusFrame(root, "TestString")
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
    serial_connector = SerialConnectorFrame(root)
    serial_connector.pack(expand=True, fill='both')
    serial_connector.set_connect_func(lambda: 
        print(f"{serial_connector.get_port()} and {serial_connector.get_baud()}"))
    root.mainloop()

def demo_all():
    demo_status_frame_grid()
    demo_led_button_grid()
    demo_status_frame()
    demo_led_button()
    demo_file_action()
    demo_serial_connector()