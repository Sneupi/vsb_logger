import tkinter as tk
from abc import ABC, abstractmethod


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
