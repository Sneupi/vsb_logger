"""
File: tkpanels.py
Author: Gabe Venegas
Purpose: tkinter for serial logging & plotter app
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import serial.tools.list_ports
from graph import LiveGraphFrame

class ControlPair(tk.Frame):
    """Frame with a button and an indicator"""
    def __init__(self, 
                 master, 
                 command:callable=None, 
                 led=False, 
                 text:str="", 
                 **kwargs):
        super().__init__(master, **kwargs)
        super().configure(width=60, height=20)
        if not command:
            command = lambda: print(f"{text}: Button not bound")
        self.led = tk.Label(self, width=2, relief="solid", borderwidth=1)
        self.button = tk.Button(self, text=text)
        self.configure(command=command, text=text, led=led)
        self.led.place(relx=0, rely=0, relwidth=0.2, relheight=1)
        self.button.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
    
    def configure(self, 
                  command: callable=None, 
                  led: bool=None, 
                  text: str=None, 
                  **kwargs):
        """Override method for tk.Frame. Allows config of led, text and 
        command appropriately, passing all other kwargs to tk.Frame.configure"""
        if command is not None:
            self.button.configure(command=command)
        if led is not None:
            self.led.configure(bg="light green" if led else "red")
        if text is not None:
            self.button.configure(text=text)
        super().configure(**kwargs)

class StatePair(tk.Frame):
    """Frame with a label and a readout field"""
    def __init__(self, 
                 master, 
                 label_text:str="???", 
                 readout_text:str="", 
                 **kwargs):
        super().__init__(master, **kwargs)
        super().configure(width=60, height=20)
        
        self.label = tk.Label(self, text=label_text)
        self.readout = tk.Label(self, 
                                text=readout_text, 
                                relief="solid", 
                                borderwidth=1, 
                                width=10)
        
        self.readout.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)  
        self.label.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    def configure(self, 
                 label_text:str=None, 
                 readout_text:str=None, 
                 **kwargs):
        """Override method for tk.Frame. Allows config of 
        label_text and readout_text appropriately, passing 
        all other kwargs to tk.Frame.configure"""
        if label_text is not None:
            self.label.configure(text=label_text)
        if readout_text is not None:
            self.readout.configure(text=readout_text)
        super().configure(**kwargs)
            
class CLIFrame(tk.Frame):
    """Command line interface"""
    def __init__(self, master, send_func=None):
        super().__init__(master)
        super().configure(width=400, height=400)
        if not send_func:
            send_func = lambda _: print("send_func not bound")
        
        self.in_str = tk.StringVar()
        self.in_txt = tk.Entry(self, textvariable=self.in_str)
        self.in_txt.config(border=5, relief="groove")
        self.in_txt.bind("<Return>", send_func)
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
        data = self.in_str.get()
        self.in_str.set("")
        return data

class VSBPanelFrame(tk.Frame):
    """Controls panel for Voltage Sense & Balance (VSB) unit"""
    def __init__(self, master):
        super().__init__(master)
        # TODO
 
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
        
        self.connect_button = ControlPair(self, text="Connect",  command=connect_func)
        self.connect_button.pack(side='right', padx=5, pady=5, fill='both', expand=True)
        
    def set_connect_func(self, func):
        self.connect_button.configure(command=func)
    
    def get_available_ports(self):
        """Get system available serial port names as list"""
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.device)
        return ports
    
    def get_port(self):
        """Get selected port name string"""
        return self.port_var.get()
    
    def get_baud(self):
        """Get selected baud rate string"""
        return self.baud_var.get()
    
    def refresh_ports(self):
        """Update dropdown with available ports"""
        self.port_options = self.get_available_ports()
        self.port_dropdown['values'] = self.port_options

class FileBrowser(tk.Frame):
    """Generic file browser Frame for selecting a 
    file and performing a specific action on it."""
    def __init__(self, master, action_name="[Action]", toggle_func=None):
        super().__init__(master)
        super().configure(width=600, height=50)
        self.log_label = tk.Label(self, text="File:")
        self.log_label.place(relx=0.3, rely=0, relwidth=0.1, relheight=1)
        
        self.browse_button = tk.Button(self, text="Select File", command=self.select_file)
        self.browse_button.place(relx=0.15, rely=0, relwidth=0.15, relheight=1)
        
        self.action_button = ControlPair(self, command=toggle_func, text=action_name)
        self.action_button.place(relx=0, rely=0, relwidth=0.15, relheight=1)
        
        self.label = tk.Label(self, borderwidth=2, relief="groove")
        self.label.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)
        
    def select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.label.config(text=path)
        
    def set_button_state(self, turn_on: bool):
        """Set state of GUI action button"""
        self.action_button.config(led=turn_on)
        
    def set_command(self, func):
        self.action_button.config(command=func)
        
    def set_action_name(self, name):
        self.action_button.config(text=name)
            
    def get_path(self):
        return self.label.cget("text")

class VSBGUI(tk.Tk):
    """GUI frontend for VSB logger & plotter"""
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title("VSB Logger")
        self.geometry("1400x700")
        self.resizable(False, False)

        self.controls = VSBPanelFrame(self)
        self.controls.place(relx=0, rely=0, relwidth=0.45, relheight=0.3)
        
        self.filebrowser = FileBrowser(self)
        self.filebrowser.place(relx=0, rely=0.3, relwidth=0.45, relheight=0.05)
                
        self.serial_setup = SerialSetup(self)
        self.serial_setup.place(relx=0, rely=0.95, relwidth=0.45, relheight=0.05)

        self.terminal = CLIFrame(self)
        self.terminal.place(relx=0.01, rely=0.36, relwidth=0.43, relheight=0.58)
        
        self.graph = LiveGraphFrame(self)
        self.graph.place(relx=0.45, rely=0.05, relwidth=0.55, relheight=0.95)
        
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
    
    def bind_terminal_send(self, func):
        """Bind function to terminal send
        
        Expects function with signature: func() -> str"""
        self.terminal.set_send_func(func)
    
    def bind_button(self, name, func):
        """Bind function to a GUI control panel button.
        
        Valid Buttons: balance, connect, debug, debug2, 
        error, extbus, info, log cpi, mq dump, run, 
        show dn, stop, trace, trace2, clear err, probe status"""
        name = name.lower()
        if name == "clear err":
            self.controls.stat.set_clear_func(func)
        elif name == "connect":
            self.serial_setup.set_connect_func(func)
        elif name == "log cpi":
            self.filebrowser.set_command("Log CPI", func)
        else:
            self.controls.bind_func(name, func)

    def update_button(self, widget_name, state: bool):
        """Update button on GUI with new state.
        
        Valid Names:
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
        - probe status"""
        
        if widget_name == "log cpi":
            self.filebrowser.set_button_state(state)
        elif widget_name == "connect":
            self.serial_setup.connect_button.configure(state)
        elif widget_name in ["balance", "extbus", "mq dump", "run", "show dn", "stop", 
                             "debug", "debug2", "error", "info", "trace", "trace2", "probe status"]:
            self.controls.set_data(widget_name, state)
    
    def update_statistic(self, widget_name, data: str):
        """Update statistic on GUI with new string.
        
        Valid Names:
        - ctc
        - dn delta
        - errs
        - last cv
        - last cv dn
        - last err
        - pvm"""
        if widget_name in ["ctc", "dn delta", "errs", "last cv", "last cv dn", "last err", "pvm"]:
            self.controls.set_data(widget_name, data)
        
    def update_terminal(self, data):
        """Insert data into terminal."""
        self.terminal.insert(data)
        
    def update_graph(self, channel: str, x: int, y: int):
        """Add new data (x, y) to graph.
        Plots and shifts graph if necessary."""
        self.graph.append(channel, y)
    
    def get_led(self, widget_name):
        """Get the state of a specific LED
        
        Valid LED names: balance, connect, debug, debug2, 
        error, extbus, info, log cpi, mq dump, run, 
        show dn, stop, trace, trace2, probe status"""
        if widget_name == "connect":
            return self.serial_setup.connect_button.is_on
        elif widget_name == "log cpi":
            return self.filebrowser.enabled
        else:
            return self.controls.get_led(widget_name)

class VSBHelpTopLevel(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.title("Help")
        self.geometry("500x500")

        self.text = tk.Text(self, wrap="word", state="disabled")
        self.text.pack(fill="both", expand=True, padx=5, pady=5)

        self.populate_help_content()

    def populate_help_content(self):
        help_content = """
Welcome to the VSB Logger Help!

(This window is scrollable)

BRIEF DESCRIPTION:
-------------------
    This application is designed to log and plot 
    serial data obtained from a Voltage Sense & 
    Balancing (VSB) unit. The key features for 
    this application have been detailed below.
        
BUTTONS PANEL:
-------------------
    A panel of VSB control buttons with LEDs 
    indicating the status of each. Each button
    is responsible for sending a respective 
    command to the VSB unit.

    Each button state (LED) is updated directly
    from the stream of incoming VSB data. 
    Meaning if the VSB unit sends a "balance" 
    command, the balance button will light up 
    only upon a confirmation string is received.

    All buttons are always initialized to off. 
    Meaning initial states may not be accurate
    if connecting to an already running VSB unit
    until the VSB unit sends respective messages
    to confirm each correct state.

STATUS PANEL:
-------------------
    Note: This panel is only live when the
    "Probe Status" button is toggled on.

    A panel of readouts for various VSB states
    taken directly from incoming VSB data strings.

LOGGING PANEL:
-------------------
    A file browser for selecting a file to log 
    data to, and a button to toggle logging on/off.
        
SERIAL TERMINAL:
-------------------
    A command-line interface for displaying, 
    receiving, and sending custom commands to the 
    VSB unit.
        
SERIAL SETUP:
-------------------
    A dropdown menu for selecting the serial port 
    and baud rate, discovering ports (refresh) and 
    connecting to a selected port. Note you may type 
    your own port name if it is not listed.
        
GRAPH PANEL:
-------------------
    A live-updating graph of the data being received 
    from the VSB unit. Displayed as raw DN (digital 
    number) values 0-4095 on an adjustable timescale.
    
    Notes: 
    - The first slider (top) controls the 
    manual scroll behavior when autoshift is off.
    - The second slider (bottom) controls the 
    width of the x-axis in the units selected.
    - Graph legend labels can be clicked to 
    toggle channel visibility.
    - The "Update Units" button must be pressed
    after changing units in the dropdown for it to
    take effect.
"""

        self.text.configure(state="normal")
        self.text.insert("1.0", help_content)
        self.text.configure(state="disabled")
        
if __name__ == "__main__":
    # Example demo
    # app = VSBGUI()
    # app.mainloop()
    
    root= tk.Tk()
    frame = FileBrowser(root)
    frame.pack(fill='both', expand=True)
    root.mainloop()