import tkinter as tk

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("VSB Logger")
        self.geometry("1400x700")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: self.quit() or self.destroy())