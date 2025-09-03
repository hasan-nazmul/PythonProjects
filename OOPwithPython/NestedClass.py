class Outer:
    class Inner:
        def __init__(self, data):
            self.inner_data = data
        def __str__(self):
            return f'Inner Data: {self.inner_data}'

    def __init__(self, data):
        self.outer_data = Outer.Inner(data)

    def show(self):
        print(self.outer_data)

o = Outer('Hoist the colors high!')
o.show()