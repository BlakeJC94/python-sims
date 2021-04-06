import argparse
import matplotlib.animation as animation
from math import pi
import numpy as np
import matplotlib.pyplot as plt

N = 10
width, height = 640, 480

pos = [width/2, height/2] + 10*np.random.rand(2*N).reshape(N, 2)
angles = 2*pi*np.random.rand(N)
vel = np.array(list(zip(np.sin(angles), np.cos(angles))))


def apply_bc(self):
    delta_r = 2.0
    for coord in self.pos:
        if coord[0] > width + delta_r:
            coord[0] = -delta_r
        if coord[0] < -delta_r:
            coord[0] = width + delta_r
        if coord[1] > height + delta_r:
            coord[1] = -delta_r
        if coord[1] < -delta_r:
            coord[1] =  height + delta_r

# drawing a boid
fig = plt.figure()
ax = plt.axes(xlim=(0, width), ylim=(0, height))
pts, = ax.plot([], [], markersize=10, c='k', marker='o', ls='None')
beak, = ax.plot([], [], markersize=4, c='r', marker='o', ls='None')
anim = animation.FuncAnimation(fig, tick, fargs=(pts, beak, boids),
                               interval=50)
