import serial
import time
import os

import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
import ttkwidgets



rest_one = 0
rest_two = 135
rest_three = 42
rest_four = 87
rest_five = 90
rest_six = 90

# Initial angles:
one_val = rest_one
two_val = rest_two
three_val = rest_three
four_val = rest_four
five_val = rest_five
six_val = rest_six

# List of ports

os.system("python -m serial.tools.list_ports")

port = '/dev/ttyUSB0'
baud = 9600

input('connect?')
arm = serial.Serial(port, baud )
arm.timeout = 2

#input('Send Test Command?')


def close():
    global arm, one_val, two_val, three_val, four_val, five_val, six_val

    one_val = rest_one
    two_val = rest_two
    three_val = rest_three
    four_val = rest_four
    five_val = rest_five
    six_val = rest_six

    string = ':' + str(one_val) + ',' + str(two_val) + ',' + str(three_val) \
        + ',' + str(four_val) + ',' + str(five_val) + ';' + str(six_val) + ';'
            
    string = bytes(string, encoding="ascii")

    arm.write(string)
    arm.close()
    exit()

def auto_update():

    global one_val, two_val, three_val, four_val, five_val, six_val

    if((one_val != one.get()) or (two_val != two.get()) or (three_val != three.get()) \
        or (four_val != four.get()) or (five_val != five.get()) or (six_val != six.get())):

        one_val = one.get()
        two_val = two.get()
        three_val = three.get()
        four_val = four.get()
        five_val = five.get()
        six_val = six.get()

        string = ':' + str(one_val) + ',' + str(two_val) + ',' + str(three_val) \
            + ',' + str(four_val) + ',' + str(five_val) + ',' + str(six_val) + ';'
            
        string = bytes(string, encoding="ascii")

        arm.write(string)
    
    gui.after(100, auto_update)

gui = tk.Tk()
font_style = Font(family="Times New Roman", size=12)

gui.title("6DOF Robotic ARM controller")
tk.Label(gui, text="Adjust the angles here", font = font_style).grid(row=0, column=0)

tk.Label(gui, text="Pan:", font = font_style).grid(row=1, column=0)
one = tk.Scale(gui, from_=0, to=180, orient= tk.HORIZONTAL)
one.grid(row = 1, column = 1)
one.set(one_val)


tk.Label(gui, text="Upper Tilt:", font = font_style).grid(row=2, column=0)
two = tk.Scale(gui, from_=0, to=180, orient= tk.HORIZONTAL)
two.grid(row = 2, column = 1)
two.set(two_val)

tk.Label(gui, text="Middle Tilt:", font = font_style).grid(row=3, column=0)
three = tk.Scale(gui, from_=0, to=180, orient= tk.HORIZONTAL)
three.grid(row = 3, column = 1)
three.set(three_val)


tk.Label(gui, text="Lower Tilt:", font = font_style).grid(row=4, column=0)
four = tk.Scale(gui, from_=0, to=180, orient= tk.HORIZONTAL)
four.grid(row = 4, column = 1)
four.set(four_val)

tk.Label(gui, text="Palm:", font = font_style).grid(row=5, column=0)
five = tk.Scale(gui, from_=0, to=180, orient= tk.HORIZONTAL)
five.grid(row = 5, column = 1)
five.set(five_val)

tk.Label(gui, text="Finger:", font = font_style).grid(row=6, column=0)
six = tk.Scale(gui, from_=0, to=180, orient= tk.HORIZONTAL)
six.grid(row = 6, column = 1)
six.set(six_val)

close_butt = tk.Button(gui, text="Close Connection", font = font_style, command= close)
close_butt.grid(row=10, column=1)

gui.after(100, auto_update)
gui.mainloop()

  