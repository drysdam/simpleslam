#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import pygame
import sys

class Line():
    def __init__(self, a, b, c):
        # ax + by + c = 0
        self.params = np.array([a, b, c])

    def show(self):
        print(self.params)

    def graph(self, ax=None):
        # ax + by + c = 0
        # -by = ax + c
        # y = -(a/b)x - c/b

        if self.params[1] == 0:
            if self.params[0] == 0:
                raise "this is not a line"
            # xa + c = 0
            x = [-1*self.params[2]/self.params[0]] * np.ones(100)
            y = np.linspace(1, 10, 100)
        else:
            x = np.linspace(1, 10, 100)
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
        print('here')
        
        
if __name__ == '__main__':
    fig, ax = plt.subplots()

    # y = 1x + 1
    l1 = Line(1, -1, 1)
    l1.graph(ax)
    # y = -1x + 1
    l2 = Line(-1, -1, 1)
    l2.graph(ax)
    # y = 0
    l3 = Line(0, 1, 0)
    l3.graph(ax)
    # x = 0
    l4 = Line(1, 0, 0)
    l4.graph(ax)

    x, y = l1.intersection(l2)
    plt.plot(x, y, 'o')
    x, y = l2.intersection(l1)
    plt.plot(x, y, 'o')
    # x, y = l1.intersection(l1)
    # plt.plot(x, y, 'o')
    x, y = l1.intersection(l3)
    plt.plot(x, y, 'o')
    # x, y = l3.intersection(l4)
    # plt.plot(x, y, 'o')
    # x, y = l3.intersection(l3)
    # plt.plot(x, y, 'o')
    
    plt.show()
