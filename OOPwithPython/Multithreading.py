from threading import *
from time import *

class MyData():
    def __init__(self):
        self.data = 1
        self.cv = Condition()

    def puts(self, data):
        self.cv.acquire()
        self.cv.wait(timeout=0)
        self.data = data
        print('Producer:', data)
        self.cv.notify()
        self.cv.release()

    def gets(self):
        self.cv.acquire()
        self.cv.wait(timeout=0)
        x = self.data
        self.cv.notify()
        self.cv.release()
        return x

def producer(data):
    a = 1
    b = 1
    n = 1
    while True:
        data.puts(n)
        a, b = b, n
        n = a+b
        sleep(1)

def consumer(data):
    while True:
        print('Consumer:', data.gets())
        sleep(1)

md = MyData()

t1 = Thread(target=lambda: producer(md))
t2 = Thread(target=lambda: consumer(md))

t1.start()
t2.start()

t1.join()
t2.join()