class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __str__(self):
        return f'x: {self.x}, y: {self.y}'

a = Vector(10, 20)
b = Vector(12, 45)
print(a+b)