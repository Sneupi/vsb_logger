"""
File: tkpanels.py
Author: Gabe Venegas
Purpose: tkinter for serial logging & plotter app
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import serial.tools.list_ports
from tkgraph import LiveGraphFrame

class ControlPair(tk.Frame):
    """Frame with a button and an indicator"""
    def __init__(self, master, button_text="N/A"):
        super().__init__(master)
        self.config(width=200, height=50)
        self.is_on = False
        self.led = tk.Label(self, width=2, relief="solid", borderwidth=1)
        self.set_led(False)
        self.button = tk.Button(self, text=button_text)
        self.led.place(relx=0, rely=0, relwidth=0.2, relheight=1)
        self.button.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
    
    def set_led(self, on: bool):
        self.led.config(bg="light green" if on else "red")
        self.is_on = on
    
    def toggle_led(self):
        self.set_led(not self.is_on)

    def set_cmd(self, command):
        """Set function called on button press"""
        self.button.config(command=command)

class SystemFrame(tk.Frame):
    """Column of system controls"""
    def __init__(self, master):
        super().__init__(master)
        
        self.run = ControlPair(self, button_text="Run")
        self.run.set_cmd(lambda: print("Run: Button function not bound"))
        self.run.place(relx=0, rely=0, relwidth=1, relheight=0.14)

        self.stop = ControlPair(self, button_text="Stop")
        self.stop.set_cmd(lambda: print("Stop: Button function not bound"))
        self.stop.place(relx=0, rely=0.14, relwidth=1, relheight=0.14)

        self.balance = ControlPair(self, button_text="Balance")
        self.balance.set_cmd(lambda: print("Balance: Button function not bound"))
        self.balance.place(relx=0, rely=0.28, relwidth=1, relheight=0.14)

        self.extbus = ControlPair(self, button_text="ExtBus")
        self.extbus.set_cmd(lambda: print("ExtBus: Button function not bound"))
        self.extbus.place(relx=0, rely=0.42, relwidth=1, relheight=0.14)

        self.mq_dump = ControlPair(self, button_text="MQ Dump")
        self.mq_dump.set_cmd(lambda: print("MQ Dump: Button function not bound"))
        self.mq_dump.place(relx=0, rely=0.56, relwidth=1, relheight=0.14)

        self.show_dn = ControlPair(self, button_text="Show DN")
        self.show_dn.set_cmd(lambda: print("Show DN: Button function not bound"))
        self.show_dn.place(relx=0, rely=0.70, relwidth=1, relheight=0.14)

        # self.connect = ControlPair(self, button_text="Connect")
        # self.connect.set_cmd(lambda: print("Connect: Button function not bound"))
        # self.connect.place(relx=0, rely=0.84, relwidth=1, relheight=0.14)

    def set_button_command(self, button_name, command):
        """Set the command for a specific button
        
        Valid button names: run, stop, balance, 
        extbus, mq dump, show dn, connect"""
        button_name = button_name.lower()
        if button_name == "run":
            self.run.set_cmd(command)
        elif button_name == "stop":
            self.stop.set_cmd(command)
        elif button_name == "balance":
            self.balance.set_cmd(command)
        elif button_name == "extbus":
            self.extbus.set_cmd(command)
        elif button_name == "mq dump":
            self.mq_dump.set_cmd(command)
        elif button_name == "show dn":
            self.show_dn.set_cmd(command)
        elif button_name == "connect":
            self.connect.set_cmd(command)
            
    def set_led(self, led_name, is_on: bool):
        """Set the state of a specific LED
        
        Valid LED names: run, stop, balance, 
        extbus, mq dump, show dn, connect"""
        led_name = led_name.lower()
        if led_name == "run":
            self.run.set_led(is_on)
        elif led_name == "stop":
            self.stop.set_led(is_on)
        elif led_name == "balance":
            self.balance.set_led(is_on)
        elif led_name == "extbus":
            self.extbus.set_led(is_on)
        elif led_name == "mq dump":
            self.mq_dump.set_led(is_on)
        elif led_name == "show dn":
            self.show_dn.set_led(is_on)
        elif led_name == "connect":
            self.connect.set_led(is_on)
            
class DiagnosticFrame(tk.Frame):
    """Column of diagnostic controls"""
    def __init__(self, master):
        super().__init__(master)
        
        self.debug = ControlPair(self, button_text="Debug")
        self.debug.set_cmd(lambda: print("Debug: Button function not bound"))
        self.debug.place(relx=0, rely=0, relwidth=1, relheight=0.14)

        self.debug2 = ControlPair(self, button_text="Debug2")
        self.debug2.set_cmd(lambda: print("Debug2: Button function not bound"))
        self.debug2.place(relx=0, rely=0.14, relwidth=1, relheight=0.14)

        self.trace = ControlPair(self, button_text="Trace")
        self.trace.set_cmd(lambda: print("Trace: Button function not bound"))
        self.trace.place(relx=0, rely=0.28, relwidth=1, relheight=0.14)

        self.trace2 = ControlPair(self, button_text="Trace2")
        self.trace2.set_cmd(lambda: print("Trace2: Button function not bound"))
        self.trace2.place(relx=0, rely=0.42, relwidth=1, relheight=0.14)

        self.info = ControlPair(self, button_text="Info")
        self.info.set_cmd(lambda: print("Info: Button function not bound"))
        self.info.place(relx=0, rely=0.56, relwidth=1, relheight=0.14)

        self.error = ControlPair(self, button_text="Error")
        self.error.set_cmd(lambda: print("Error: Button function not bound"))
        self.error.place(relx=0, rely=0.70, relwidth=1, relheight=0.14)

        # self.log_cpi = ControlPair(self, button_text="Log CPI")
        # self.log_cpi.set_cmd(lambda: print("Log CPI: Button function not bound"))
        # self.log_cpi.place(relx=0, rely=0.84, relwidth=1, relheight=0.14)

    def set_button_command(self, button_name, command):
        """Set the command for a specific button
        
        Valid button names: debug, debug2, trace, 
        trace2, info, error, log cpi"""
        button_name = button_name.lower()
        if button_name == "debug":
            self.debug.set_cmd(command)
        elif button_name == "debug2":
            self.debug2.set_cmd(command)
        elif button_name == "trace":
            self.trace.set_cmd(command)
        elif button_name == "trace2":
            self.trace2.set_cmd(command)
        elif button_name == "info":
            self.info.set_cmd(command)
        elif button_name == "error":
            self.error.set_cmd(command)
        elif button_name == "log cpi":
            self.log_cpi.set_cmd(command)
            
    def set_led(self, led_name, is_on: bool):
        """Set the state of a specific LED
        
        Valid LED names: debug, debug2, trace, 
        trace2, info, error, log cpi"""
        led_name = led_name.lower()
        if led_name == "debug":
            self.debug.set_led(is_on)
        elif led_name == "debug2":
            self.debug2.set_led(is_on)
        elif led_name == "trace":
            self.trace.set_led(is_on)
        elif led_name == "trace2":
            self.trace2.set_led(is_on)
        elif led_name == "info":
            self.info.set_led(is_on)
        elif led_name == "error":
            self.error.set_led(is_on)
        elif led_name == "log cpi":
            self.log_cpi.set_led(is_on)

class StatePair(tk.Frame):
    """Frame with a label and a readout field"""
    def __init__(self, master, label_text="N/A"):
        super().__init__(master)
        
        self.label = tk.Label(self, text=label_text)
        self.readout = tk.Label(self, text="", relief="solid", borderwidth=1, width=10)  # Set a fixed width for the window
        
        self.readout.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)  
        self.label.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    def update(self, new_text):
        """Update the readout text"""
        self.readout.config(text=new_text)

class StateFrame(tk.Frame):
    """Column of status readouts"""
    def __init__(self, master):
        super().__init__(master)
        
        self.num_errs = int(0)
        
        self.pvm = StatePair(self, label_text="PVM State")
        self.pvm.place(relx=0, rely=0, relwidth=1, relheight=0.125)

        self.ctc = StatePair(self, label_text="CTC State")
        self.ctc.place(relx=0, rely=0.125, relwidth=1, relheight=0.125)

        self.last_cv = StatePair(self, label_text="Last CV")
        self.last_cv.place(relx=0, rely=0.25, relwidth=1, relheight=0.125)

        self.last_cv_dn = StatePair(self, label_text="Last CV DN")
        self.last_cv_dn.place(relx=0, rely=0.375, relwidth=1, relheight=0.125)

        self.errs = StatePair(self, label_text="Err Count")
        self.errs.place(relx=0, rely=0.75, relwidth=1, relheight=0.125)

        self.last_err = StatePair(self, label_text="Last Error")
        self.last_err.place(relx=0, rely=0.625, relwidth=1, relheight=0.125)
        
        self.dn_delta = StatePair(self, label_text="DN Delta")
        self.dn_delta.place(relx=0, rely=0.5, relwidth=1, relheight=0.125)
        
        self.clr_err_button = tk.Button(self, text="Clr Err Count", command=self._clear_errs)
        self.clr_err_button.place(relx=0.5, rely=0.875, relwidth=0.5, relheight=0.125)
        
    def set_state(self, state_name, new_text):
        """Set the state of a specific readout
        
        Valid state names: pvm, ctc, last cv, 
        last cv dn, errs, last err, dn delta"""
        state_name = state_name.lower()
        if state_name == "pvm":
            self.pvm.update(new_text)
        elif state_name == "ctc":
            self.ctc.update(new_text)
        elif state_name == "last cv":
            self.last_cv.update(new_text)
        elif state_name == "last cv dn":
            self.last_cv_dn.update(new_text)
        elif state_name == "errs":
            self.errs.update(new_text)
        elif state_name == "last err":
            self.last_err.update(new_text)
        elif state_name == "dn delta":
            self.dn_delta.update(new_text)
        
    def _clear_errs(self):
        # FIXME not thread safe 
        self.num_errs = 0
        self.errs.update(self.num_errs)
        
    def _incr_errs(self):
        # FIXME not thread safe
        self.num_errs += 1
        self.errs.update(self.num_errs)        

class CLIFrame(tk.Frame):
    """Command line interface"""
    def __init__(self, master, send_func=None):
        super().__init__(master)
        
        self.in_str = tk.StringVar()
        self.in_txt = tk.Entry(self, textvariable=self.in_str)
        self.in_txt.config(border=5, relief="groove")
        self.in_txt.bind("<Return>", send_func if send_func else lambda _: print("Terminal send function not bound"))
        self.in_txt.place(relx=0, rely=0.8, relwidth=1, relheight=0.15)
        
        self.out_txt = tk.Text(self, bg="black", fg="white")
        self.out_txt.config(state=tk.DISABLED)
        self.out_txt.place(relx=0, rely=0, relwidth=1, relheight=0.8)
        
        self.clr_button = tk.Button(self, text="Clear Terminal", command=self.clear)
        self.clr_button.place(relx=0.66, rely=0.95, relwidth=0.33, relheight=0.05)
        
        self.is_scroll = True
        self.scroll_button = tk.Button(self, text="Scroll OFF", command=self.pause_scroll)
        self.scroll_button.place(relx=0.33, rely=0.95, relwidth=0.33, relheight=0.05)

    def set_send_func(self, send_func):
        """Set the function called on <Return>"""
        self.in_txt.bind("<Return>", send_func)
    
    def clear(self):
        """Clear the terminal"""
        self.out_txt.config(state=tk.NORMAL)
        self.out_txt.delete("1.0", tk.END)
        self.out_txt.config(state=tk.DISABLED)
    
    def insert(self, msg: str):
        """Insert a message into the terminal"""
        self.out_txt.config(state=tk.NORMAL)
        self.out_txt.insert(tk.END, "> {}\n".format(msg.rstrip('\n')))
        self.out_txt.config(state=tk.DISABLED)
        if self.is_scroll:
            self.out_txt.see(tk.END)
            
    def pause_scroll(self):
        """Toggle the scroll state"""
        # FIXME not thread safe (i think)
        self.is_scroll = not self.is_scroll
        self.scroll_button.config(text="Scroll {}".format("OFF" if self.is_scroll else "ON"))
        if self.is_scroll:
            self.out_txt.see(tk.END)
        
    def get_entry(self):
        """NOTE: Clears entry after returns"""
        data = self.in_str.get() + '\n'
        self.in_str.set("")
        return data

class ControlsFrame(tk.Frame):
    """Controls panel, with system, diagnostic, and status columns"""
    def __init__(self, master):
        super().__init__(master)
        self.sys = SystemFrame(self)
        self.diag = DiagnosticFrame(self)
        self.stat = StateFrame(self)
        
        self.sys.place(relx=0, rely=0, relwidth=0.33, relheight=1)
        self.diag.place(relx=0.33, rely=0, relwidth=0.33, relheight=1)
        self.stat.place(relx=0.66, rely=0, relwidth=0.34, relheight=1)
        
    def set_data(self, widget_name, data):
        """Update GUI widget with new data.
        
        Valid Datatype (per widget):
        - State: str
        - Button: bool
        
        Valid Buttons:
        - balance
        - connect
        - debug
        - debug2
        - error
        - extbus
        - info
        - log cpi
        - mq dump
        - run
        - show dn
        - stop
        - trace
        - trace2
        
        Valid States:
        - ctc
        - dn delta
        - errs
        - last cv
        - last cv dn
        - last err
        - pvm"""
        widget_name = widget_name.lower()
        if widget_name in ["balance", "connect", "extbus", "mq dump", "run", "show dn", "stop"]:
            if isinstance(data, bool):
                self.sys.set_led(widget_name, data)
            else:
                raise TypeError("Invalid data type for button widget. Expected bool.")
            
        elif widget_name in ["debug", "debug2", "error", "info", "log cpi", "trace", "trace2"]:
            if isinstance(data, bool):
                self.diag.set_led(widget_name, data)
            else:
                raise TypeError("Invalid data type for button widget. Expected bool.")
            
        elif widget_name in ["ctc", "dn delta", "errs", "last cv", "last cv dn", "last err", "pvm"]:
            if isinstance(data, str):
                self.stat.set_state(widget_name, data)
            else:
                raise TypeError("Invalid data type for state widget. Expected str.")
            
        else:
            raise ValueError("Invalid widget name.")
    
    def bind_func(self, widget_name, func):
        """Bind function to GUI button
        
        Valid Buttons: 
        balance, connect, debug, debug2, error, extbus, info, 
        log cpi, mq dump, run, show dn, stop, trace, trace2"""
        widget_name = widget_name.lower()
        if widget_name in ["balance", "connect", "extbus", "mq dump", "run", "show dn", "stop"]:
            self.sys.set_button_command(widget_name, func)
        elif widget_name in ["debug", "debug2", "error", "info", "log cpi", "trace", "trace2"]:
            self.diag.set_button_command(widget_name, func)
        else:
            raise ValueError("Invalid widget name.")
 
class SerialSetup(tk.Frame):
    """User interface for setting up serial connection
    
    NOTE: User should bind a connect function 
    to the connect button that has the signature:
    func(port: str, baud: int) -> bool"""
    def __init__(self, parent, connect_func=None):
        super().__init__(parent)
        
        self.port_label = tk.Label(self, text="Port:")
        self.port_label.pack(side='left', padx=5, pady=5)
        
        self.port_options = self.get_available_ports()
        self.port_var = tk.StringVar(self)
        if self.port_options:
            self.port_var.set(self.port_options[0])
        self.port_dropdown = ttk.Combobox(self, textvariable=self.port_var, values=self.port_options)
        self.port_dropdown.pack(side='left', padx=5, pady=5)
        
        self.baud_label = tk.Label(self, text="Baud:")
        self.baud_label.pack(side='left', padx=5, pady=5)

        self.baud_options = ['9600', '19200', '38400', '57600', '115200']
        self.baud_var = tk.StringVar(self)
        self.baud_var.set(self.baud_options[4])
        self.baud_dropdown = ttk.Combobox(self, textvariable=self.baud_var, values=self.baud_options)
        self.baud_dropdown.pack(side='left', padx=5, pady=5)
        
        self.refresh_button = tk.Button(self, text="Refresh Ports", command=self.refresh_ports)
        self.refresh_button.pack(side='right', padx=5, pady=5)
        
        self.connect_func = connect_func
        self.connect_button = ControlPair(self, button_text="Connect")
        self.connect_button.set_cmd(self.connect)
        self.connect_button.pack(side='right', padx=5, pady=5)
        
    def bind_connect(self, func):
        self.connect_func = func
        
    def connect(self):
        """Internal function to connect to serial port,
        allowing button state to be updated."""
        if not self.connect_func:
            print("Connect function not bound.")
            return
        
        port = self.get_port()
        baud = self.get_baud()
        
        if port and baud:
            try:
                ok = self.connect_func(port, baud)
                self.connect_button.set_led(ok)
            except Exception as e:
                print(f"SerialSetup Error: {e}")
    
    def get_available_ports(self):
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.device)
        return ports
    
    def get_port(self):
        return self.port_var.get()
    
    def get_baud(self):
        return self.baud_var.get()
    
    def refresh_ports(self):
        self.port_options = self.get_available_ports()
        self.port_dropdown['values'] = self.port_options

class FileBrowser(tk.Frame):
    """Generic file browser Frame for selecting a 
    file and performing a specific action on it.
    
    NOTE: User should declare a toggle 
    function that returns a bool"""
    def __init__(self, master, action_name="[Action]", toggle_func=None):
        super().__init__(master)
        self.log_label = tk.Label(self, text="File:")
        self.log_label.place(relx=0.3, rely=0, relwidth=0.1, relheight=1)
        
        self.browse_button = tk.Button(self, text="Select File", command=self.select_file)
        self.browse_button.place(relx=0, rely=0, relwidth=0.15, relheight=1)
        
        self.action_button = tk.Button(self, command=self.toggle_action)
        self.bind_action(action_name, toggle_func)
        self.action_button.place(relx=0.15, rely=0, relwidth=0.15, relheight=1)
        
        self.label = tk.Label(self, borderwidth=2, relief="groove")
        self.label.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)
        
    def select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.label.config(text=path)
    
    def toggle_action(self):
        """Execute the toggle_function bound to the button.
        
        Expected function signature: func() -> bool"""
        if not self.toggle_func:
            print("Action function not bound.")
            return
        self.set_button_state(self.toggle_func())
        
    def set_button_state(self, turn_on: bool):
        """Set state of GUI action button"""
        self.enabled = turn_on
        self.action_button.config(bg="light green" if turn_on else "red")
        self.action_button.config(text="{} {}".format(self.action_name, "ON" if turn_on else "OFF"))
        
    def bind_action(self, action_name, toggle_func):
        self.action_name = action_name
        self.toggle_func = toggle_func
        self.enabled = False
        self.set_button_state(self.enabled)
            
    def get_path(self):
        return self.label.cget("text")

class VSBGUI(tk.Tk):
    """GUI frontend for VSB logger & plotter"""
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title("VSB Logger")
        self.geometry("1400x700")
        self.resizable(False, False)

        self.controls = ControlsFrame(self)
        self.controls.place(relx=0, rely=0, relwidth=0.45, relheight=0.3)
        
        self.filebrowser = FileBrowser(self)
        self.filebrowser.place(relx=0, rely=0.3, relwidth=0.45, relheight=0.05)
                
        self.serial_setup = SerialSetup(self)
        self.serial_setup.place(relx=0, rely=0.95, relwidth=0.45, relheight=0.05)

        self.terminal = CLIFrame(self)
        self.terminal.place(relx=0.01, rely=0.36, relwidth=0.43, relheight=0.58)
        
        self.graph = LiveGraphFrame(self)
        self.graph.place(relx=0.45, rely=0.05, relwidth=0.55, relheight=1)
        
        self.help_button = tk.Button(self, text="HELP", command=self.spawn_help)
        self.help_button.place(relx=0.8, rely=0, relwidth=0.1, relheight=0.05)
        
        self.exit_button = tk.Button(self, text="EXIT")
        self.exit_button.place(relx=0.9, rely=0, relwidth=0.1, relheight=0.05)

        self.call_on_exit(None)  # Default behavior
        
    def call_on_exit(self, func=None):
        """If func not None, calls function 
        following default exit behavior."""
        cmd = lambda: self.quit() or self.destroy() or (func() if func else None)
        self.exit_button.config(command=cmd) 
        self.protocol("WM_DELETE_WINDOW", cmd)
    
    def spawn_help(self):
        """Spawn a help window"""
        help_window = VSBHelpTopLevel(self)

    def bind_exit(self, func):
        """Bind custom function on exit"""
        self.exit_button.config(command=func)
        self.protocol("WM_DELETE_WINDOW", func)
    
    def bind_button(self, name, func):
        """Bind function to a GUI control panel button.
        
        Valid Buttons: balance, connect, debug, debug2, 
        error, extbus, info, log cpi, mq dump, run, 
        show dn, stop, trace, trace2"""
        self.controls.bind_func(name, func)

    def update_control(self, widget_name, data):
        """Update widget on control panel with new data."""
        self.controls.set_data(widget_name, data)
        
    def update_terminal(self, data):
        """Insert data into terminal."""
        self.terminal.insert(data)
        
    def update_graph(self, channel: str, x: int, y: int):
        """Add new data (x, y) to graph.
        Plots and shifts graph if necessary."""
        self.graph.add_datapoint(channel, x, y)

class VSBHelpTopLevel(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.title("Help")
        self.geometry("400x300")

        self.text = tk.Text(self, wrap="word", state="disabled")
        self.text.pack(fill="both", expand=True)

        self.populate_help_content()

    def populate_help_content(self):
        help_content = """
        Welcome to the VSB Logger Help!

        (I still need to write this part...)

        Thank you for using VSB Logger!
        """

        self.text.configure(state="normal")
        self.text.insert("1.0", help_content)
        self.text.configure(state="disabled")
        
if __name__ == "__main__":
    # Example demo
    app = VSBGUI()
    app.mainloop()