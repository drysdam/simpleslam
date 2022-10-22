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
    
class World():
    def __init__(self, polygonmap):
        self.pgonmap = polygonmap
        self.ax = None

    def graph(self):
        print(self.pgonmap)
        sgdraw.draw(self.pgonmap)
    
    def probe(self, position, angle, noise=0, dropout=0):
        # ray = sg.Ray2(sg.Point2(0, 0),
        #               sg.Point2(10, 0))
        origin = sg.Point2(position[0], position[1])
        ray = sg.Ray2(origin, deg2dir(angle))
        #sgdraw.draw(ray, display_range=100)
        mind = 1e10
        for edge in self.pgonmap.edges:
            isct = sg.intersection(ray, edge)
            if isct == None:
                continue
            d = np.sqrt(float((isct - origin).squared_length()))
            mind = min(mind, d)

        if np.random.random(1) < dropout:
            return None
        return mind + noise*np.random.random(1)-noise/2.
    
if __name__ == '__main__':    
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot(121)

    pgon = sg.Polygon([sg.Point2(-50, 50),
                       sg.Point2(50, 50),
                       sg.Point2(50, -50),
                       sg.Point2(-50, -50)])
    W = World(pgon)
    W.graph()

    angs = range(0, 360, 1)
    #angs = [0, 45, 90]
    plotangs = []
    rngs = []
    for ang in angs:
        #ax.clear()
        rng = W.probe([0, 0], ang, noise=1.0, dropout=.15)
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
    axp.plot(np.deg2rad(plotangs), rngs,
             '.', markersize=3)
        
    ax.set_ylim(-100,100)
    ax.set_xlim(-100,100)
    plt.show()
