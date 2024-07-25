import tkinter as tk

class LEDButton(tk.Frame):
    """Frame with a button and an indicator"""
    def __init__(self, master, text:str=""):
        super().__init__(master)
        super().configure(width=100, height=27)
        default_command = lambda: print(f"{text}: Button not bound")
        
        self.led = tk.Label(self, width=2, relief="solid", borderwidth=1)
        self.set_led(False)
        self.led.place(relx=0, rely=0, relwidth=0.2, relheight=1)
        
        self.button = tk.Button(self, text=text)
        self.button.configure(command=default_command, text=text)
        self.button.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
    
    def set_command(self, command):
        self.button.configure(command=command)

    def set_led(self, state: bool):
        self.led.configure(bg="light green" if state else "red")
        
    def get_led(self) -> bool:
        """Get the state of the LED"""
        return self.led.cget("bg") == "light green"