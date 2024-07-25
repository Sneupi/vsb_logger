import tkinter as tk

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
        self.is_scroll = not self.is_scroll
        self.scroll_button.config(text="Scroll {}".format("OFF" if self.is_scroll else "ON"))
        if self.is_scroll:
            self.out_txt.see(tk.END)
        
    def get_entry(self):
        """NOTE: Clears entry after returns"""
        data = self.in_str.get()
        self.in_str.set("")
        return data

class CLIView(CLIFrame):
    """Command line interface"""
    # just a wrapper for naming consistency
