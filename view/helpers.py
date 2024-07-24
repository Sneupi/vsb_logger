"""
File: tkpanels.py
Author: Gabe Venegas
Purpose: tkinter for serial logging & plotter app
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import serial.tools.list_ports
from .graphing import LiveGraphTk
from abc import ABC, abstractmethod
import re


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
    
        self.config = self.configure  # Alias for configure
    
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
        
    def get_led(self) -> bool:
        """Get the state of the LED"""
        return self.led.cget("bg") == "light green"

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
        
        self.config = self.configure  # Alias for configure

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

class WidgetGrid(tk.Frame, ABC):
    def __init__(self, master, widget_class, list2D):
        """list2D: list of lists of 
        strings ordered [column][row]"""
        super().__init__(master)
        self.widgets = {}
        self.widget_class = widget_class
        for col_ndx, col in enumerate(list2D):
            for row_ndx, name in enumerate(col):
                self.widgets[name] = self._instantiation(name)
                self.widgets[name].grid(row=row_ndx, column=col_ndx, sticky='nsew')
                self.rowconfigure(row_ndx, weight=1)
                self.columnconfigure(col_ndx, weight=1)
                
    @abstractmethod
    def _instantiation(self, text) -> tk.Widget:
        """Instantiate a widget constructing as needed"""
        pass
    
    def get_widgets(self) -> dict:
        return self.widgets
    
class ControlPairGrid(WidgetGrid):
    def __init__(self, master, list2D):
        super().__init__(master, ControlPair, list2D)
    def _instantiation(self, text) -> tk.Widget:
        return ControlPair(self, text=text)
    
class StatePairGrid(WidgetGrid):
    def __init__(self, master, list2D):
        super().__init__(master, StatePair, list2D)
    def _instantiation(self, text) -> tk.Widget:
        return StatePair(self, label_text=text)

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
        
        self.connect_name = "Connect"
        self.connect_button = ControlPair(self, text=self.connect_name,  command=connect_func)
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
        self.name = action_name
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
        self.name = name
            
    def get_path(self):
        return self.label.cget("text")
               
class VSBPanelFrame(tk.Frame):
    """Controls panel for Voltage Sense & Balance (VSB) unit"""
    def __init__(self, master):
        super().__init__(master)
        
        
        # list[column][row] of each type
        ctrl_names = [["Run", "Stop", "Balance", "ExtBus", "MQ Dump", "Show DN"], 
                      ["Debug", "Debug2", "Trace", "Trace2", "Info", "Error"]]
        stat_names = [["PVM", "CTC", "Last CV", "Last CV DN", "Last Err", "Errs"]]
        
        self.ctrl_grid = ControlPairGrid(self, ctrl_names)
        self.ctrl_grid.pack(side='left', fill='both', expand=True)
        self.stat_grid = StatePairGrid(self, stat_names)  
        self.stat_grid.pack(side='left', fill='both', expand=True)
        
    def get_controlpairs(self) -> dict:
        return self.ctrl_grid.get_widgets()
    
    def get_statepairs(self) -> dict:
        return self.stat_grid.get_widgets()

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
        