from tkinter import *
import time

class Stopwatch:
    def __init__(self, win):
        self.timer = Label(win, text='00:00:000', font=('times new roman', 45), bg='black', fg='white')
        self.start = Button(win, text='start', bg='green', fg='white', command=self.start_handler)
        self.stop = Button(win, text='stop', bg='red', fg='white', command=self.stop_handler)
        self.reset = Button(win, text='reset', bg='blue', fg='white', command=self.reset_handler)
        self.flag = True
        self.elapsed_time = 0
        self.starting_time = 0
        self.timer.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        self.start.grid(row=2, column=1, padx=5, pady=5)
        self.stop.grid(row=2, column=2, padx=5, pady=5)
        self.reset.grid(row=2, column=3, padx=5, pady=5)

    def update_watch(self):
        inc = int(self.flag) * int(round((time.time() - self.starting_time)*1000))
        self.starting_time = time.time()
        tm = self.elapsed_time
        self.elapsed_time += inc
        mn, sc, ms = (tm // 60000), (tm % 60000) // 1000, (tm % 1000)
        self.timer['text'] = f'{mn:0>2}:{sc:0>2}:{ms:0>3}'
        self.timer.after(10, self.update_watch)

    def start_handler(self):
        self.starting_time = time.time()
        self.flag = True
        self.update_watch()

    def stop_handler(self):
        self.flag = False

    def reset_handler(self):
        self.elapsed_time = 0
        self.flag = False

win = Tk()
win.title('Stopwatch')
win.geometry('800x600')

sw = Stopwatch(win)

win.mainloop()