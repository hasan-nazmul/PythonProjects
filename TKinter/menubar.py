from tkinter import *

def myhandler():
    txt1.insert(1.0, 'Hello World')

def pophandler(e):
    file.tk_popup(e.x_root, e.y_root)

win = Tk()
win.geometry('800x600')

txt1 = Text(win)
txt1.pack(fill=BOTH)

menubar = Menu()
win['menu'] = menubar

file = Menu(menubar)
menubar.add_cascade(label='File', menu=file)

file.add_command(label='New', command=myhandler)
file.add_command(label='Open')
file.add(itemType='command', label='Save')
file.add_separator()
file.add_checkbutton(label='Save as', onvalue=1, offvalue=0)

rad1 = Menu(file)
rad1.add_radiobutton(label='option 1')
rad1.add_radiobutton(label='option 2')
rad1.add_radiobutton(label='option 3')
file.add_cascade(label='Options', menu=rad1)

txt1.bind('<Button-3>', pophandler)

win.mainloop()