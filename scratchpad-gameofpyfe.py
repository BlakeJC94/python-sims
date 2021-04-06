import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim


# represent grid
x = np.array([[0, 0, 255], [255, 255, 0], [0, 255, 0]])
plt.imshow(x, interpolation='nearest')
plt.show()  # with default colormap, off is purple and on is yellow


# random initial conditions
p = 0.9
N = 4
x = np.random.choice([0, 255], N**2, p=[1-p, p]).reshape(N, N)
plt.imshow(x, interpolation='nearest')
plt.show()


# adding gliders
def add_glider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider
N = 6
grid = np.zeros(N**2).reshape(N, N)
add_glider(2, 2, grid)
plt.imshow(grid, interpolation='nearest')
plt.show()



