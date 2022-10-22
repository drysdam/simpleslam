#!/usr/bin/env python3

import skgeom as sg
import skgeom.draw as sgdraw
import numpy as np
import matplotlib.pyplot as plt
import sys

def deg2dir(ang):
    # 0 is up, 90 to the right
    rad = np.deg2rad(ang)
    s = np.sin(rad)
    c = np.cos(rad)
    dir2 = sg.Direction2(100*s, 100*c)
    print(ang, rad, s, c, dir2)
    return dir2
    
class Map():
    def __init__(self, polygon):
        self.pgon = polygon
        self.ax = None

    def graph(self):
        print(self.pgon)
        sgdraw.draw(self.pgon)
    
    def probe(self, position, angle):
        # ray = sg.Ray2(sg.Point2(0, 0),
        #               sg.Point2(10, 0))
        origin = sg.Point2(position[0], position[1])
        ray = sg.Ray2(origin, deg2dir(angle))
        #sgdraw.draw(ray, display_range=100)
        mind = 1e10
        for edge in self.pgon.edges:
            isct = sg.intersection(ray, edge)
            if isct == None:
                continue
            d = np.sqrt(float((isct - origin).squared_length()))
            mind = min(mind, d)

        return mind
    
if __name__ == '__main__':    
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot(121)

    pgon = sg.Polygon([sg.Point2(-50, 50),
                       sg.Point2(50, 50),
                       sg.Point2(50, -50),
                       sg.Point2(-50, -50)])
    mp = Map(pgon)
    mp.graph()

    angs = range(0, 360)
    #angs = [0, 45, 90]
    plotangs = []
    rngs = []
    for ang in angs:
        #ax.clear()
        rng = mp.probe([0, -10], ang)
        if rng == None:
            continue
        plotangs.append(ang)
        rngs.append(rng)
        #mp.graph()

    for ang, rng in zip(plotangs, rngs):
        print(ang, rng)
        
    axp = fig.add_subplot(122, projection='polar')
    axp.set_theta_direction(-1)
    axp.set_theta_offset(np.pi / 2.0)
    axp.plot(np.deg2rad(plotangs), rngs)
        
    ax.set_ylim(-100,100)
    ax.set_xlim(-100,100)
    plt.show()
