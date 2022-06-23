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

def points2general(xy1, xy2):
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
        
class Line():
    def __init__(self, A, B, C):
        # Ax + By + C = 0
        self.params = np.array([A, B, C])

    def show(self):
        print(self.params)

    def graph(self, size=201, ax=None):
        # Ax + By + C = 0
        # -By = Ax + C
        # y = -(A/B)x - C/B

        A, B, C = self.params
        if B == 0:
            if A == 0:
                raise "this is not a line"
            # Ax + C = 0
            x = [-1*C/A] * np.ones(size)
            y = np.linspace(-1*(size-1)/2.0, (size-1)/2.0, size)
        else:
            x = np.linspace(-1*(size-1)/2.0, (size-1)/2.0, 201)
            y = -1*A/B * x - C/B

        if ax == None:
            fig, ax = plt.subplots()
        ax.plot(x, y)

    def inbounds(self, xy):
        return True
        
    def intersection(self, l2):
        # https://www.cuemath.com/geometry/intersection-of-two-lines/
        # I bet linear algebra would actually be faster...
        # ((B1C2 - B2C1)/(A1B2 - A2B1), (C1A2 - C2A1)/(A1B2 - A2B1))
        A1, B1, C1 = self.params
        A2, B2, C2 = l2.params
        num1 = B1*C2 - B2*C1
        num2 = C1*A2 - C2*A1
        denom = A1*B2 - A2*B1

        # lines are parallel
        if denom == 0:
            return None

        xy = [num1/float(denom), num2/float(denom)]
        if self.inbounds(xy) and l2.inbounds(xy):
            return np.array(xy)
        return None

class Ray(Line):
    def __init__(self, xyorigin, angle):
        self.xy = xyorigin
        self.angle = angle
        
        
        x1, y1 = xyorigin
        if angle < 90 or angle > 270:
            print('case 1')
            x2 = x1 + 100
            y2 = y1 + (x2-x1) * np.tan(np.deg2rad(angle))
            print(x1, y1)
            print(x2, y2)
        elif angle > 90 and angle < 270:
            print('case 2')
            x2 = x1 - 100
            y2 = y1 + (x2-x1) * np.tan(np.deg2rad(angle))
        elif angle == 90:
            print('case 3')
            x2 = x1
            y2 = y1 + 100
        elif angle == 270:
            print('case 4')
            x2 = x1
            y2 = y1 - 100
        else:
            raise 'what'

        self.params = np.array(points2general(xyorigin, [x2,y2]))

    def graph(self, size=101, ax=None):
        x = self.xy[0] + np.linspace(-1*(size-1)/2.0, (size-1)/2.0, 201)
        y = np.tan(np.deg2rad(self.angle)) * x
        ax.plot(x, y)
        
class Segment(Line):
    def __init__(self, xy1, xy2):
        self.xy1 = xy1
        self.xy2 = xy2

        self.params = np.array(points2general(xy1, xy2))

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

    def inbounds(self, xy):
        x, y = xy
        if (x < min(self.xy1[0], self.xy2[0])
            or x > max(self.xy1[0], self.xy2[0])
            or y < min(self.xy1[1], self.xy2[1])
            or y > max(self.xy1[1], self.xy2[1])):
            return False
        return True

    def intersection(self, l2):
        try:
            x, y = Line.intersection(self, l2)
        except TypeError:
            return None

        if self.inbounds([x, y]) and l2.inbounds([x, y]):
            return np.array([x, y])
        return None
        
if __name__ == '__main__':
    fig, ax = plt.subplots()

    # # y = 1x + 10
    # l1 = Line(1, -1, 10)
    # # y = -1x + 10
    # l2 = Line(-1, -1, 10)
    # # y = 30
    # l3 = Line(0, 1, -30)
    # # x = 50
    # l4 = Line(1, 0, -50)

    # s1 = Segment((-10,40), (10,40))
    # s2 = Segment((5,10), (5,20))

    # for la in [l1, l2, l3, l4, s1, s2]:
    #     la.graph(size=101, ax=ax)
    #     for lb in [l1, l2, l3, l4, s1, s2]:
    #         try:
    #             x, y = la.intersection(lb)
    #         except TypeError:
    #             continue
    #         plt.plot(x, y, 'o')

    r1 = Ray([0, 0], 270+1)
    r1.graph(size=101, ax=ax)
    
    ax.set_ylim(-100,100)
    ax.set_xlim(-100,100)
    plt.show()
