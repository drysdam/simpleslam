#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import pygame
import sys

def float_gcd(a, b, rtol = 1e-05, atol = 1e-08):
    t = min(abs(a), abs(b))
    while abs(b) > rtol * t + atol:
        a, b = b, a % b
    return a

# print(float_gcd(100, 10))
# print(float_gcd(100, 10.1))
# print(float_gcd(100, 11.0))
# print(float_gcd(100, 2.5))
# sys.exit(0)

class Line():
    def __init__(self, a, b, c):
        # ax + by + c = 0
        self.params = np.array([a, b, c])

    def show(self):
        print(self.params)

    def graph(self, size=201, ax=None):
        # ax + by + c = 0
        # -by = ax + c
        # y = -(a/b)x - c/b

        if self.params[1] == 0:
            if self.params[0] == 0:
                raise "this is not a line"
            # xa + c = 0
            x = [-1*self.params[2]/self.params[0]] * np.ones(size)
            y = np.linspace(-1*(size-1)/2.0, (size-1)/2.0, size)
        else:
            x = np.linspace(-1*(size-1)/2.0, (size-1)/2.0, 201)
            y = -1*self.params[0]/self.params[1] * x - self.params[2]/self.params[1]

        if ax == None:
            fig, ax = plt.subplots()
        ax.plot(x, y)

    def intersection(self, l2):
        # https://www.cuemath.com/geometry/intersection-of-two-lines/
        # I bet linear algebra would actually be faster...
        # ((b1c2 - b2c1)/(a1b2 - a2b1), (c1a2 - c2a1)/(a1b2 - a2b1))
        a1, b1, c1 = self.params
        a2, b2, c2 = l2.params
        num1 = b1*c2 - b2*c1
        num2 = c1*a2 - c2*a1
        denom = a1*b2 - a2*b1

        # lines are parallel
        if denom == 0:
            return None

        return np.array([num1/float(denom), num2/float(denom)])

class Segment(Line):
    def __init__(self, xy1, xy2):
        self.xy1 = xy1
        self.xy2 = xy2

        self.params = np.array(self._convert2params(xy1, xy2))

    def _convert2params(self, xy1, xy2):
        x1,y1 = xy1
        x2,y2 = xy2
        # (x1, y1) ... (x2, y2)

        try:
            m = (y2 - y1)/(x2 - x1)
        except ZeroDivisionError:
            # B = 0
            # AX + C = 0
            # X = -C/A
            return [1, 0, -1*x1]
        
        # by similar triangles
        # (y2-b)/(x2-0) = (y2-y1)/(x2-x1) = m
        # b = y2 - mx2
        b = y2 - m * x2
        
        # Ax + By + C = 0
        # -By = Ax + C
        # y = -(A/B)x - C/B
        # m = -(A/B)
        # b = -(C/B)
        B = float_gcd(m, b)
        A = -1*m*B
        C = -1*b*B
        return [A, B, C]
        
    def graph(self, size=201, ax=None):
        x = np.linspace(min(self.xy1[0], self.xy2[0]),
                        max(self.xy1[0], self.xy2[0]),
                        size)
        y = np.linspace(min(self.xy1[1], self.xy2[1]),
                        max(self.xy1[1], self.xy2[1]),
                        size)

        if ax == None:
            fig, ax = plt.subplots()
        ax.plot(x, y)

    def intersection(self, l2):
        try:
            x, y = Line.intersection(self, l2)
        except TypeError:
            return None

        if (x < min(self.xy1[0], self.xy2[0])
            or x > max(self.xy1[0], self.xy2[0])
            or y < min(self.xy1[1], self.xy2[1])
            or y > max(self.xy1[1], self.xy2[1])):
            return None

        try:
            l2xy1, l2xy2 = l2.xy1, l2.xy2
        except AttributeError:
            return np.array([x, y])

        if (x < min(l2xy1[0], l2xy2[0])
            or x > max(l2xy1[0], l2xy2[0])
            or y < min(l2xy1[1], l2xy2[1])
            or y > max(l2xy1[1], l2xy2[1])):
            return None
        
        return np.array([x, y])
        
if __name__ == '__main__':
    fig, ax = plt.subplots()

    # y = 1x + 10
    l1 = Line(1, -1, 10)
    # y = -1x + 10
    l2 = Line(-1, -1, 10)
    # y = 30
    l3 = Line(0, 1, -30)
    # x = 50
    l4 = Line(1, 0, -50)

    for la in [l1, l2, l3, l4]:
        la.graph(size=101, ax=ax)
        for lb in [l1, l2, l3, l4]:
            try:
                x, y = la.intersection(lb)
            except TypeError:
                continue
            plt.plot(x, y, 'o')

    s1 = Segment((-10,40), (10,40))
    s2 = Segment((5,10), (5,20))
    for sa in [s1, s2]:
        sa.graph(ax=ax)
        for sb in [s1, s2]:
            try:
                x, y = sa.intersection(sb)
            except TypeError:
                continue
            plt.plot(x, y, 'o')
    
    plt.show()
