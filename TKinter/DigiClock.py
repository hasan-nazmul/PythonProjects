from tkinter import *
from datetime import *

win = Tk()
win.title('Digital Clock')
win.geometry('800x600')

class DigitalClock:
    def __init__(self, win, x, y):
        self.label = Label(win, font=('Times new roman', 20), bg='green', fg='purple')
        self.label.place(x=x, y=y)

    def ticking(self):
        self.label['text'] = datetime.now().strftime('%I:%M:%S')
        self.label.after(100, self.ticking)

dc1 = DigitalClock(win=win, x=10, y=10)
dc2 = DigitalClock(win=win, x=200, y=200)

dc1.ticking()
dc2.ticking()

win.mainloop()