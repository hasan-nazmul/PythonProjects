class Rectangle:
    def __init__(self, length=1, breadth=1):
        self.length = length
        self.breadth = breadth

    def area(self):
        return self.length * self.breadth

    def perimeter(self):
        return 2 * (self.length+self.breadth)

class Cuboid(Rectangle):
    def __init__(self, length=1, breadth=1, height=1):
        super().__init__(length, breadth)
        self.height = height

    def volume(self):
        return self.length * self.breadth * self.height

c = Cuboid(10, 10, 10)

print(c.area(), c.perimeter(), c.volume())