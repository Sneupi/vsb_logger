"""
File: tkpanels.py
Author: Gabe Venegas
Purpose: Contains the classes for the GUI panels
         to be used in the VSB GUI.
"""

import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

class ControlPair(tk.Frame):
    """Frame with a button and an indicator"""
    def __init__(self, master, button_text="N/A"):
        super().__init__(master)
        
        self.led = tk.Label(self, width=2, relief="solid", borderwidth=1)
        self.set_led(False)
        self.button = tk.Button(self, text=button_text)
        self.led.place(relx=0, rely=0, relwidth=0.2, relheight=1)
        self.button.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
    
    def set_led(self, on: bool):
        self.led.config(bg="light green" if on else "red")

class SystemFrame(tk.Frame):
    """Column of system controls"""
    def __init__(self, master):
        super().__init__(master)
        
        self.run = ControlPair(self, button_text="Run")
        self.run.button.config(command=self.__run)
        self.run.place(relx=0, rely=0, relwidth=1, relheight=0.14)

        self.stop = ControlPair(self, button_text="Stop")
        self.stop.button.config(command=self.__stop)
        self.stop.place(relx=0, rely=0.14, relwidth=1, relheight=0.14)

        self.balance = ControlPair(self, button_text="Balance")
        self.balance.button.config(command=self.__balance)
        self.balance.place(relx=0, rely=0.28, relwidth=1, relheight=0.14)

        self.extbus = ControlPair(self, button_text="ExtBus")
        self.extbus.button.config(command=self.__extbus)
        self.extbus.place(relx=0, rely=0.42, relwidth=1, relheight=0.14)

        self.mq_dump = ControlPair(self, button_text="MQ Dump")
        self.mq_dump.button.config(command=self.__mq_dump)
        self.mq_dump.place(relx=0, rely=0.56, relwidth=1, relheight=0.14)

        self.cp_lock = ControlPair(self, button_text="CP Lock")
        self.cp_lock.button.config(command=self.__cp_lock)
        self.cp_lock.place(relx=0, rely=0.70, relwidth=1, relheight=0.14)

        self.connect = ControlPair(self, button_text="Connect")
        self.connect.button.config(command=self.__connect)
        self.connect.place(relx=0, rely=0.84, relwidth=1, relheight=0.14)

    def __run(self):
        # TODO: Run button action
        print("Run button clicked")

    def __stop(self):
        # TODO: Stop button action
        print("Stop button clicked")

    def __balance(self):
        # TODO: Balance button action
        print("Balance button clicked")

    def __extbus(self):
        # TODO: ExtBus button action
        print("ExtBus button clicked")

    def __mq_dump(self):
        # TODO: MQ Dump button action
        print("MQ Dump button clicked")

    def __cp_lock(self):
        # TODO: CP Lock button action
        print("CP Lock button clicked")

    def __connect(self):
        # TODO: Connect button action
        print("Connect button clicked")        

class DiagnosticFrame(tk.Frame):
    """Column of diagnostic controls"""
    def __init__(self, master):
        super().__init__(master)
        
        self.debug = ControlPair(self, button_text="Debug")
        self.debug.button.config(command=self.__debug)
        self.debug.place(relx=0, rely=0, relwidth=1, relheight=0.14)

        self.debug2 = ControlPair(self, button_text="Debug2")
        self.debug2.button.config(command=self.__debug2)
        self.debug2.place(relx=0, rely=0.14, relwidth=1, relheight=0.14)

        self.trace = ControlPair(self, button_text="Trace")
        self.trace.button.config(command=self.__trace)
        self.trace.place(relx=0, rely=0.28, relwidth=1, relheight=0.14)

        self.trace2 = ControlPair(self, button_text="Trace2")
        self.trace2.button.config(command=self.__trace2)
        self.trace2.place(relx=0, rely=0.42, relwidth=1, relheight=0.14)

        self.info = ControlPair(self, button_text="Info")
        self.info.button.config(command=self.__info)
        self.info.place(relx=0, rely=0.56, relwidth=1, relheight=0.14)

        self.error = ControlPair(self, button_text="Error")
        self.error.button.config(command=self.__error)
        self.error.place(relx=0, rely=0.70, relwidth=1, relheight=0.14)

        self.log_cpi = ControlPair(self, button_text="Log CPI")
        self.log_cpi.button.config(command=self.__log_cpi)
        self.log_cpi.place(relx=0, rely=0.84, relwidth=1, relheight=0.14)

    def __debug(self):
        # TODO: Debug button action
        print("Debug button clicked")

    def __debug2(self):
        # TODO: Debug2 button action
        print("Debug2 button clicked")

    def __trace(self):
        # TODO: Trace button action
        print("Trace button clicked")

    def __trace2(self):
        # TODO: Trace2 button action
        print("Trace2 button clicked")

    def __info(self):
        # TODO: Info button action
        print("Info button clicked")

    def __error(self):
        # TODO: Error button action
        print("Error button clicked")

    def __log_cpi(self):
        # TODO: Log CPI button action
        print("Log CPI button clicked")

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
        self.pvm.place(relx=0, rely=0, relwidth=1, relheight=0.14)

        self.ctc = StatePair(self, label_text="CTC State")
        self.ctc.place(relx=0, rely=0.14, relwidth=1, relheight=0.14)

        self.last_cv = StatePair(self, label_text="Last CV")
        self.last_cv.place(relx=0, rely=0.28, relwidth=1, relheight=0.14)

        self.last_cv_dn = StatePair(self, label_text="Last CV DN")
        self.last_cv_dn.place(relx=0, rely=0.42, relwidth=1, relheight=0.14)

        self.errs = StatePair(self, label_text="Err Count")
        self.errs.place(relx=0, rely=0.56, relwidth=1, relheight=0.14)

        self.last_err = StatePair(self, label_text="Last Error")
        self.last_err.place(relx=0, rely=0.70, relwidth=1, relheight=0.14)
        
        self.clr_err_button = tk.Button(self, text="Clr Err Count", command=self._clear_errs)
        self.clr_err_button.place(relx=0.5, rely=0.84, relwidth=0.5, relheight=0.14)
        
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
    def __init__(self, master, send_func):
        super().__init__(master)
        
        self.in_str = tk.StringVar()
        self.in_txt = tk.Entry(self, textvariable=self.in_str)
        self.in_txt.bind("<Return>", send_func)
        self.in_txt.place(relx=0, rely=0.8, relwidth=1, relheight=0.1)
        
        self.out_txt = tk.Text(self, bg="black", fg="white")
        self.out_txt.config(state=tk.DISABLED)
        self.out_txt.place(relx=0, rely=0, relwidth=1, relheight=0.8)
        
        self.clr_button = tk.Button(self, text="Clear", command=self.clear)
        self.clr_button.place(relx=0.66, rely=0.9, relwidth=0.33, relheight=0.1)
        
        self.is_scroll = True
        self.scroll_button = tk.Button(self, text="Scroll OFF", command=self.pause_scroll)
        self.scroll_button.place(relx=0.33, rely=0.9, relwidth=0.33, relheight=0.1)
        
    def clear(self):
        """Clear the terminal"""
        self.out_txt.config(state=tk.NORMAL)
        self.out_txt.delete("1.0", tk.END)
        self.out_txt.config(state=tk.DISABLED)
    
    def log_message(self, msg: str):
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
 
class SerialSetup(tk.Frame):
    """User interface for setting up serial connection"""
    def __init__(self, parent, connect_func):
        super().__init__(parent)
        
        self.port_label = tk.Label(self, text="Port:")
        self.port_label.pack(side='left', padx=5, pady=5)
        
        self.port_options = self.get_available_ports()
        self.port_var = tk.StringVar(self)
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

        self.connect_button = tk.Button(self, text="Connect", command=connect_func)
        self.connect_button.bind('<Return>', connect_func)
        self.connect_button.pack(side='right', padx=5, pady=5)
        
        self.refresh_button = tk.Button(self, text="Refresh", command=self.refresh_ports)
        self.refresh_button.pack(side='right', padx=5, pady=5)
    
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
