import tkinter as tk

class StatusBox(tk.Frame):
    """Frame with a label and a readout field"""
    def __init__(self, master, text:str="???"):
        super().__init__(master)
        super().configure(width=100, height=40)
        
        self.label = tk.Label(self, text=text)
        self.readout = tk.Label(self, relief="solid", 
                                borderwidth=1, width=10)
        
        self.readout.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)  
        self.label.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    def set_readout(self, text):
        self.readout.configure(text=text)


