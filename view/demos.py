import tkinter as tk
from .controls import VSBControls
from .widgets.file_action import FileAction
from .help import HelpWindow

def demo_controls():
    root = tk.Tk()
    controls = VSBControls(root)
    controls.pack(expand=True, fill='both')
    
    controls.set_button_command("Run", lambda: controls.set_led("Run", not controls.get_led("Run")))
    controls.set_button_command("Stop", lambda: controls.set_led("Stop", not controls.get_led("Stop")))
    controls.set_button_command("Balance", lambda: controls.set_led("Balance", not controls.get_led("Balance")))
    controls.set_button_command("ExtBus", lambda: controls.set_led("ExtBus", not controls.get_led("ExtBus")))
    controls.set_button_command("MQ Dump", lambda: controls.set_led("MQ Dump", not controls.get_led("MQ Dump")))
    controls.set_button_command("Show DN", lambda: controls.set_led("Show DN", not controls.get_led("Show DN")))
    controls.set_button_command("Debug", lambda: controls.set_led("Debug", not controls.get_led("Debug")))
    controls.set_button_command("Debug2", lambda: controls.set_led("Debug2", not controls.get_led("Debug2")))
    controls.set_button_command("Trace", lambda: controls.set_led("Trace", not controls.get_led("Trace")))
    controls.set_button_command("Trace2", lambda: controls.set_led("Trace2", not controls.get_led("Trace2")))
    controls.set_button_command("Info", lambda: controls.set_led("Info", not controls.get_led("Info")))
    controls.set_button_command("Error", lambda: controls.set_led("Error", not controls.get_led("Error")))
    
    def recursive_counter(n=0):
        for i, name in enumerate(controls.get_statuses().keys()):
            controls.set_readout(name, f"{n+i}")
        root.after(1000, recursive_counter, n+1)
    recursive_counter()
    root.mainloop()

def demo_log():
    root = tk.Tk()
    log = FileAction(root, text="(Some Logger)")
    log.pack(expand=True, fill='both')
    def example_setup_log_func():
        print("test toggling the log...")
        log.set_button_state(not log.get_button_state())
    log.set_command(example_setup_log_func)
    root.mainloop()

def demo_help():
    root = tk.Tk()
    button = tk.Button(root, text="Help", command=lambda: HelpWindow(root))
    button.pack(expand=True, fill='both', padx=10, pady=10)
    root.mainloop()
    
def demo_all():
    demo_controls()
    demo_log()
    demo_help()