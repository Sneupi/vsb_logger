import tkinter as tk
from tkinter import ttk
from .widgets.serial_connector import SerialConnector
import serial.tools.list_ports

class SerialView(SerialConnector):
    """View for serial connector menu"""
    # wrapper just for naming consistency
    pass