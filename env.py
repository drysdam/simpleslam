#!/usr/bin/env python3

import skgeom as sg
import skgeom.draw as sgdraw
import numpy as np
import matplotlib.pyplot as plt
import sys

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
        origin = sg.Point2(0, 0)
        ray = sg.Ray2(origin, sg.Direction2(100, ang))
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

    axp = fig.add_subplot(122, projection='polar')

    angs = range(0, 360)
    plotangs = []
    rngs = []
    for ang in angs:
        #ax.clear()
        rng = mp.probe([0, 0], ang)
        if rng == None:
            continue
        plotangs.append(ang)
        rngs.append(rng)
        #mp.graph()

    print(plotangs)
    print(rngs)
    axp.plot(np.deg2rad(plotangs), rngs)
        
    ax.set_ylim(-100,100)
    ax.set_xlim(-100,100)
    plt.show()
