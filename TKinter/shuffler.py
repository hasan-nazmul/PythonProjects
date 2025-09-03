from tkinter import *
from random import shuffle

def shuffler():
    global items
    shuffle(items)
    var.set(value=items)

def show(e):
    lbl['text'] = txt.get(txt.curselection())

win = Tk()
win.geometry('600x400')
win.title('Base Conversion')

items = ['C', 'C++', 'Python', 'Java', 'Pearl', 'PHP', 'Javascript', 'Ruby on Rails']

lbl = Label(win, text='Select Item', font=('Arial', 20))
lbl.pack()

var = Variable(value=items)
txt = Listbox(win, listvariable=var, font=('Arial', 15))
txt.pack()
txt.bind('<<ListboxSelect>>', show)

btn = Button(win, text='Shuffle', pady=10, font=('Arial', 10), width=15, command=shuffler)
btn.pack()

win.mainloop()
