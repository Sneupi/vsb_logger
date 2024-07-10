import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

auto_shift = True
X_WIDTH = 10
Y_HEIGHT = 4095

def data_gen(t=0):
    cnt = 0
    while cnt < 2000:
        cnt += 1
        t += 0.1
        yield t, t*10  # np.sin(2*np.pi*t) * np.exp(-t/10.)


def init():
    ax.set_ylim(0, Y_HEIGHT)
    ax.set_xlim(0, X_WIDTH)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
line, = ax.plot([], [], lw=2)
ax.grid()
xdata, ydata = [], []


# Slider code
axcolor = 'lightgoldenrodyellow'
axpos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)

spos = Slider(axpos, 'Pos', 0, 1)

def update(val):
    if not auto_shift:
        mx = max(xdata)
        mn = min(xdata)
        pos = mn + (spos.val * (mx - mn))
        ax.set_xlim(pos-X_WIDTH//2,pos+X_WIDTH//2)
        ax.figure.canvas.draw()
        # fig.canvas.draw_idle()

spos.on_changed(update)


# Animation code
def run(data):
    t, y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()
    
    mx = max(xdata)
    if auto_shift and mx >= xmax:
        ax.set_xlim(mx-X_WIDTH, mx)
        ax.figure.canvas.draw()
        
    line.set_data(xdata, ydata)

    return line,


# Tkinter code
root = tk.Tk()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

def toggle_auto_shift():
    global auto_shift
    auto_shift = not auto_shift
    auto_shift_button.config(text="Shift ON" if auto_shift else "Shift OFF")
    if not auto_shift:
        update(0)  # Update with current slider value
        
auto_shift_button = tk.Button(root, text="Shift ON", command=toggle_auto_shift)
auto_shift_button.pack()

def clear_data():
    del xdata[:]
    del ydata[:]
clear_data_button = tk.Button(root, text="Clear Data", command=clear_data)
clear_data_button.pack()

ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=10,
                              repeat=False, init_func=init)
root.protocol("WM_DELETE_WINDOW", lambda: root.quit() or root.destroy())
root.mainloop()

print("end")