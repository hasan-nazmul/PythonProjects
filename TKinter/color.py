from sysconfig import get_config_var
from tkinter import *
from random import shuffle

def rgb_handler(e):
    r_val = hex(int(red.get()))
    g_val = hex(int(green.get()))
    b_val = hex(int(blue.get()))
    rgb = f'#{r_val[2:]:0>2}{g_val[2:]:0>2}{b_val[2:]:0>2}'
    color['bg'] = rgb

win = Tk()
win.geometry('600x400')
win.title('Base Conversion')

color = Label(win, bg='black', width=20)
color.grid(row=0, columnspan=5)

l1 = Label(win, text='Red')
red = Scale(win, from_=0, to=255, bg='red', orient=HORIZONTAL, command=rgb_handler)
l2 = Label(win, text='Green')
green = Scale(win, from_=0, to=255, bg='green', orient=HORIZONTAL, command=rgb_handler)
l3 = Label(win, text='Blue')
blue = Scale(win, from_=0, to=255, bg='blue', orient=HORIZONTAL, command=rgb_handler)

l1.grid(row=1, column=0)
red.grid(row=1, column=1)
l2.grid(row=2, column=0)
green.grid(row=2, column=1)
l3.grid(row=3, column=0)
blue.grid(row=3, column=1)

win.mainloop()
