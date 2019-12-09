class Quaternion:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.norm = (a**2 + b**2 + c**2 + d**2)**0.5
        self.norm_sqr = self.norm**2

    def __str__(self):
        q_str1 = f'{self.a} ' + '{0:+}i '.format(self.b)
        q_str2 = '{0:+}j '.format(self.c) + '{0:+}k '.format(self.d)
        return q_str1 + q_str2

    def __repr__(self):
        return f'({self.a}, {self.b}, {self.c}, {self.d})'

    def __add__(self, other):
        a = self.a + other.a
        b = self.b + other.b
        c = self.c + other.c
        d = self.d + other.d
        result = Quaternion(a, b, c, d)
        return result

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            a = (other.a*self.a - other.b*self.b - other.c*self.c - other.d*self.d)
            b = (other.a*self.b + other.b*self.a - other.c*self.d + other.d*self.c)
            c = (other.a*self.c + other.b*self.d + other.c*self.a - other.d*self.b)
            d = (other.a*self.d - other.b*self.c + other.c*self.b + other.d*self.a)
        elif isinstance(other, (int, float)):
            a = self.a * other
            b = self.b * other
            c = self.c * other
            d = self.d * other
        else:
            return 'Invalid multiplier! Please enter a number or a quaternion.'
        result = Quaternion(a, b, c, d)
        return result

    def __truediv__(self, other):
        if isinstance(other, Quaternion):
            inv_a = self.a / self.norm_sqr
            inv_b = -self.b / self.norm_sqr
            inv_c = -self.c / self.norm_sqr
            inv_d = -self.d / self.norm_sqr

            a = (other.a*inv_a - other.b*inv_b - other.c*inv_c - other.d*inv_d)
            b = (other.a*inv_b + other.b*inv_a - other.c*inv_d + other.d*inv_c)
            c = (other.a*inv_c + other.b*inv_d + other.c*inv_a - other.d*inv_b)
            d = (other.a*inv_d - other.b*inv_c + other.c*inv_b + other.d*inv_a)
        elif isinstance(other, (int, float)):
            a = self.a / other
            b = self.b / other
            c = self.c / other
            d = self.d / other
        else:
            return 'Invalid divisor! Please enter a number or a quaternion.'
        result = Quaternion(a, b, c, d)
        return result

    def __mod__(self, irrelevant):
        """
        The quaternion norm calculation doesn't require an additional parameter,
        but in order to provide the functionality using the '%' operator, the
        'irrelevant' argument was added.
        """
        return self.norm

    def __eq__(self, other):
        if isinstance(other, Quaternion):
            q = self.a == other.a
            x = self.b == other.b
            y = self.c == other.c
            z = self.d == other.d
            return q and x and y and z
        else:
            return ('Incomparable values!')
