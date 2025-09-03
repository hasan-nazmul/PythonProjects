from tkinter import *
from decimal import Decimal

def update():
    value = int(num.get())
    base_dict = {10: Decimal, 2: bin, 8: oct, 16: hex}
    value = base_dict[int(base.get())](value)
    num.delete(0, END)
    num.insert(0, value)

win = Tk()
win.geometry('600x400')
win.title('Base Conversion')

num = Entry(win)
num.grid(row=0, column=0, columnspan=4)

base = IntVar(value=10)
decimal = Radiobutton(win, text='Decimal', variable=base, value=10, command=update)
binary = Radiobutton(win, text='Binary', variable=base, value=2, command=update)
octal = Radiobutton(win, text='Octal', variable=base, value=8, command=update)
hexadecimal = Radiobutton(win, text='Hexadecimal', variable=base, value=16, command=update)

decimal.grid(row=1, column=0)
binary.grid(row=1, column=1)
octal.grid(row=1, column=2)
hexadecimal.grid(row=1, column=3)

win.mainloop()
