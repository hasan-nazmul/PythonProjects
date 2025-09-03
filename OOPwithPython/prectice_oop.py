import math

class Rational:

    def __init__(self, p, q):

        self.p = p // math.gcd(p, q)
        self.q = q // math.gcd(p, q)

    def __add__(self, other):
        p = self.p * other.q + other.p * self.q
        q = self.q * other.q
        return Rational(p, q)

    def __str__(self):
        return f'{self.p}/{self.q}'

r1 = Rational(10, 15)
r2 = Rational(9, 3)

print(r1, '+', r2, '=', r1+r2)

