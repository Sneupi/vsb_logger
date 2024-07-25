import tkinter as tk
from .cli import CLIView
from .controls import ControlsView
from .log import LogView
from .help import HelpView

def demo_cli():
    root = tk.Tk()
    cli = CLIView(root)
    cli.pack(expand=True, fill='both')
    def recursive_counter(n=0):
        cli.insert(f"{n} seconds have passed")
        root.after(1000, recursive_counter, n+1)
    def example_send_func(event):
        cli.insert(cli.get_entry())
    cli.set_send_func(example_send_func)
    recursive_counter()
    root.mainloop()

def demo_controls():
    root = tk.Tk()
    controls = ControlsView(root)
    controls.pack(expand=True, fill='both')
    
    def toggle_run():
        print("Run")
        controls.set_led("Run", not controls.get_led("Run"))

    def toggle_stop():
        print("Stop")
        controls.set_led("Stop", not controls.get_led("Stop"))

    def toggle_balance():
        print("Balance")
        controls.set_led("Balance", not controls.get_led("Balance"))

    def toggle_extbus():
        print("ExtBus")
        controls.set_led("ExtBus", not controls.get_led("ExtBus"))

    def toggle_mq_dump():
        print("MQ Dump")
        controls.set_led("MQ Dump", not controls.get_led("MQ Dump"))

    def toggle_show_dn():
        print("Show DN")
        controls.set_led("Show DN", not controls.get_led("Show DN"))

    def toggle_debug():
        print("Debug")
        controls.set_led("Debug", not controls.get_led("Debug"))

    def toggle_debug2():
        print("Debug2")
        controls.set_led("Debug2", not controls.get_led("Debug2"))

    def toggle_trace():
        print("Trace")
        controls.set_led("Trace", not controls.get_led("Trace"))

    def toggle_trace2():
        print("Trace2")
        controls.set_led("Trace2", not controls.get_led("Trace2"))

    def toggle_info():
        print("Info")
        controls.set_led("Info", not controls.get_led("Info"))

    def toggle_error():
        print("Error")
        controls.set_led("Error", not controls.get_led("Error"))

    controls.set_button_command("Run", toggle_run)
    controls.set_button_command("Stop", toggle_stop)
    controls.set_button_command("Balance", toggle_balance)
    controls.set_button_command("ExtBus", toggle_extbus)
    controls.set_button_command("MQ Dump", toggle_mq_dump)
    controls.set_button_command("Show DN", toggle_show_dn)
    controls.set_button_command("Debug", toggle_debug)
    controls.set_button_command("Debug2", toggle_debug2)
    controls.set_button_command("Trace", toggle_trace)
    controls.set_button_command("Trace2", toggle_trace2)
    controls.set_button_command("Info", toggle_info)
    controls.set_button_command("Error", toggle_error)
    
    def recursive_counter(n=0):
        for i, name in enumerate(controls.get_statuses().keys()):
            controls.set_readout(name, f"{n+i}")
        root.after(1000, recursive_counter, n+1)
    recursive_counter()
    root.mainloop()

def demo_log():
    root = tk.Tk()
    log = LogView(root)
    log.pack(expand=True, fill='both')
    def example_setup_log_func():
        print("test toggling the log...")
        log.set_button_state(not log.get_button_state())
    log.set_command(example_setup_log_func)
    root.mainloop()

def demo_help():
    root = tk.Tk()
    button = tk.Button(root, text="Help", command=lambda: HelpView(root))
    button.pack(expand=True, fill='both', padx=10, pady=10)
    root.mainloop()