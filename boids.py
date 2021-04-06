import argparse
from math import pi
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial.distance import squareform, pdist, cdist
from numpy.linalg import norm
from numpy.random import rand

width, height = 640, 480

class BoidsSim(object):
    def __init__(self, N):
        """Initialise simulation"""
        # initial positions and vleocities
        self.pos = [width/2, height/2] + 10*np.random.rand(2*N).reshape(N, 2)
        angles = 2*pi*rand(N)
        self.vel = np.array(list(zip(np.sin(angles), np.cos(angles))))
        self.N = N
        # min approach dist
        self.min_dist = 25.0
        # maxmagnitude of velocities calculated by rules
        self.max_rule_vel = 1.0
        # max magnitude of final velocity
        self.max_vel = 5.0


    def limit(self, X, max_val):
        """ilimit magnitude of 2D vectors in array X to max_val"""
        for vec in X:
            mag = norm(vec)
            if mag > max_val:
                vec[0], vec[1] = vec[0]*max_val/mag, vec[1]*max_val/mag

    def apply_bc(self):
        """apply tiled boundary conditions"""
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

    def apply_rules(self):
        """apply rules of boids simulaiton"""
        # rule 1: seperation
        D = self.dist_matrix < 25.0
        vel1 = self.pos*D.sum(axis=1).reshape(self.N, 1) - D.dot(self.pos)
        self.limit(vel1, self.max_rule_vel)
        # rule 2: alignment
        D = self.dist_matrix < 50.0  # diffennt threshold from seperation
        vel2 = D.dot(self.vel)
        self.limit(vel2, self.max_rule_vel)
        # rule 3: cohesion
        vel3 = D.dot(self.pos) - self.pos
        self.limit(vel3, self.max_rule_vel)
        return vel1 + vel2 + vel3

    def tick(self, frame_num, pts, beak):
        """Update sim by one timestep"""
        # get pairwise distances
        self.dist_matrix = squareform(pdist(self.pos))
        # apply rules
        self.vel += self.apply_rules()
        self.limit(self.vel, self.max_vel)
        self.pos += self.vel
        self.apply_bc()
        # update data
        pts.set_data(self.pos.reshape(2*self.N)[::2],
                     self.pos.reshape(2*self.N)[1::2])
        vec = self.pos + 10*self.vel/self.max_vel
        beak.set_data(vec.reshape(2*self.N)[::2],
                      vec.reshape(2*self.N)[1::2])

    def button_press(self, event):
        """event hanfdler for matplotlib button press"""
        # left click to add boid
        if event.button == 1:
            self.pos = np.concatenate((self.pos,
                                       np.array([[event.xdata, event.ydata]])),
                                      axis=0)
            # gen rand vel
            angles = angles = 2*pi*rand(1)
            v = np.array(list(zip(np.sin(angles), np.cos(angles))))
            self.vel = np.concatenate((self.vel, v), axis=0)
            self.N += 1
        # right click to scatter boids
        elif event.button == 3:
            self.vel += 0.1*(self.pos - np.array([[event.xdata, event.ydata]]))


def tick(frame_num, pts, beak, boids):
    """update function for animation"""
    boids.tick(frame_num, pts, beak)
    return pts, beak


def main():
    parser = argparse.ArgumentParser(description="Implementing Craig Reynolds Boids...")
    parser.add_argument('--num-boids', dest='N', required=False)
    args = parser.parse_args()
    #set initial number of boids
    N = 100
    if args.N:
        N = int(args.N)

    # create boids
    boids = BoidsSim(N)

    # set up plot
    fig = plt.figure()
    ax = plt.axes(xlim=(0, width), ylim=(0, height))

    pts, = ax.plot([], [], markersize=10, c='k', marker='o', ls='None')
    beak, = ax.plot([], [], markersize=4, c='r', marker='o', ls='None')
    anim = animation.FuncAnimation(fig, tick, fargs=(pts, beak, boids),
                               interval=50)

    # add button press handles
    cid = fig.canvas.mpl_connect('button_press_event', boids.button_press)

    plt.show()


if __name__ == '__main__':
    main()

