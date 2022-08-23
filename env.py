#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
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
        # print('Line params:', self.params)

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
        # print('My params:', self.params)
        # print('Their params:', l2.params)
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
        self.angle = np.fmod(angle+360, 360)

        if self.angle <= 90 or self.angle >= 270:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.angle > 180:
            self.ydir = -1
        else:
            self.ydir = 1
        
        x1, y1 = xyorigin
        if self.angle < 90 or self.angle > 270:
            x2 = 100
            y2 = y1 + x2 * np.tan(np.deg2rad(self.angle))
            x2 += x1
        elif self.angle > 90 and self.angle < 270:
            x2 = - 100
            y2 = y1 + x2 * np.tan(np.deg2rad(self.angle))
            x2 += x1
        elif self.angle == 90:
            x2 = x1
            y2 = y1 + 100
        elif self.angle == 270:
            x2 = x1
            y2 = y1 - 100
        else:
            raise 'what'

        self.params = np.array(points2general(xyorigin, [x2,y2]))
        # print('Ray points:', xyorigin + [x2, y2])
        # print('Ray params:', self.params)
        
    def graph(self, size=101, ax=None):
        if self.angle == 90 or self.angle == 270:
            if self.ydir == 1:
                y = np.linspace(0, size, size)
            else:
                y = np.linspace(-size, 0, size)
            x = 1/np.tan(np.deg2rad(self.angle)) * y
        else:
            if self.xdir == 1:
                x = np.linspace(0, size, size)
            else:
                x = np.linspace(-size, 0, size)
            y = np.tan(np.deg2rad(self.angle)) * x
        ax.plot(x + self.xy[0], y + self.xy[1])
        
    def inbounds(self, xy):
        x, y = xy
        if self.xdir == 1 and x < self.xy[0]:
            return False
        if self.xdir == -1 and x > self.xy[0]:
            return False
        if self.ydir == 1 and y < self.xy[1]:
            return False
        if self.ydir == -1 and y > self.xy[1]:
            return False
        return True

# l1params = points2general([-1,-1], [1, 1])
# l1params = points2general([-1,0], [1, 2])
# l1params = points2general([2,-2], [2, 2])
# print(l1params)
# l2params = points2general([-1,1], [1, -1])
# l2params = points2general([-1,2], [1, 0])
# l2params = points2general([0, 0], [2, 2])
# print(l2params)
# #sys.exit(0)

# fig, ax = plt.subplots()
# l1 = Line(*l1params)
# l1.graph(size=101, ax=ax)
# l2 = Line(*l2params)
# l2 = Ray([1, 0], 45)
# l2.graph(size=101, ax=ax)
# try:
#     x, y = l1.intersection(l2)
#     print(x, y)
#     plt.plot(x, y, 'o')
# except TypeError:
#     pass
# ax.set_ylim(-3,3)
# ax.set_xlim(-3,3)

# plt.show()
# sys.exit(0)

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

class Map():
    def __init__(self, walls):
        self.walls = walls

    def graph(self, ax, intersections=False):
        for i, wall in enumerate(self.walls):
            wall.graph(size=101, ax=ax)
            if intersections:
                for wall2 in self.walls[i+1:]:
                    try:
                        x, y = wall.intersection(wall2)
                        #print(x, y)
                    except TypeError:
                        continue
                    ax.plot(x, y, 'o')
                
if __name__ == '__main__':    
    fig, ax = plt.subplots()

    s1 = Segment((-50, 50), (50, 50))
    s2 = Segment((50, 50), (50, -50))
    s3 = Segment((50, -50), (-50, -50))
    s4 = Segment((-50, -50), (-50, 50))
    walls = [s1, s2, s3, s4]
    mp = Map(walls)
    mp.graph(ax, True)
    
    # ls = []
    
    # # # y = 1x + 10
    # # ls.append(Line(1, -1, 10))
    # # # y = -1x + 10
    # # ls.append(Line(-1, -1, 10))
    # # # y = 30
    # # ls.append(Line(0, 1, -30))
    # # x = 50
    # ls.append(Line(1, 0, -50))
    # ls.append(Line(1, 0, 50))
    
    # # ls.append(Segment((-10,40), (10,40)))
    # # ls.append(Segment((5,10), (5,20)))

    # #ls.append(Ray([0, 0], 45))
    # #ls.append(Line(-1, 1, 0))
    # ls.append(Ray([10, 0], 45))
    # ls.append(Ray([10, 0], -45))
    # ls.append(Ray([10, 0], 180+45))
    # ls.append(Ray([10, 0], 180+-45))
    # #ls.append(Line(1.21, -1.1, -12.1))
    # #ls.append(Ray([10, 10], 350))

    # for la in ls:
    #     la.graph(size=101, ax=ax)
    #     for lb in ls[1:]:
    #         if lb == la:
    #             continue
    #         try:
    #             x, y = la.intersection(lb)
    #             #print(x, y)
    #         except TypeError:
    #             continue
    #         ax.plot(x, y, 'o')

    ax.set_ylim(-100,100)
    ax.set_xlim(-100,100)
    plt.show()
