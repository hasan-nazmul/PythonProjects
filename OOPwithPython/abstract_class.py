from abc import ABC, abstractmethod

class Parent(ABC):
    def method1(self):
        print('Parent method -- 1')

    @abstractmethod
    def method2(self):
        pass

class Child(Parent):
    def method2(self):
        print('Child (abstract) method -- 2')
    def method3(self):
        print('Child method -- 3')

c = Child()
c.method1()
c.method2()
c.method3()