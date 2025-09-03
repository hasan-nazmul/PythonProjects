from tkinter import *
from tkinter.font import *

win = Tk()

win.geometry('300x200')
win.title('Font Options')

def update_label():
    b = 'bold' if varbold.get() == 1 else 'normal'
    i = 'italic' if varitalic.get() == 1 else 'roman'
    fnt = Font(family='Times new Roman', size=45, weight=b, slant=i, underline=varunderline.get())
    lbl['font'] = fnt

lbl = Label(win, text='Hello World', font=('Times New Roman', 45))
lbl.grid(row=0, column=0, columnspan=3)

varbold = IntVar()
bold = Checkbutton(win, text='Bold', variable=varbold, command=update_label)
varitalic = IntVar()
italic = Checkbutton(win, text='Italic', variable=varitalic, command=update_label)
varunderline = IntVar()
underline = Checkbutton(win, text='Underlined', variable=varunderline, command=update_label)

bold.grid(row=1, column=0)
italic.grid(row=1, column=1)
underline.grid(row=1, column=2)

win.mainloop()