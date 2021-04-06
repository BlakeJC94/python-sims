import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

ON = 255
OFF = 0
vals = [ON, OFF]
N_min = 42

def add_glider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[OFF, OFF, ON],
                       [ON,  OFF, ON],
                       [OFF, ON,  ON]])
    grid[i:i+3, j:j+3] = glider
    return grid

def add_gosper(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    gosper = np.zeros(11*38).reshape(11, 38)
    gosper[5:7, 1:3] = ON
    gosper[3:5, -3:-1] = ON
    gosper[3:6, 21:23] = ON
    gosper[3:10, 11:19] = np.array([[OFF, OFF, ON, ON, OFF, OFF, OFF, OFF],
                                    [OFF, ON, OFF, OFF, OFF, ON, OFF, OFF],
                                    [ON, OFF, OFF, OFF, OFF, OFF, ON, OFF],
                                    [ON, OFF, OFF, OFF, ON, OFF, ON, ON],
                                    [ON, OFF, OFF, OFF, OFF, OFF, ON, OFF],
                                    [OFF, ON, OFF, OFF, OFF, ON, OFF, OFF],
                                    [OFF, OFF, ON, ON, OFF, OFF, OFF, OFF]])
    gosper[1:3, 23:26] = np.array([[OFF, OFF, ON],
                                   [ON, OFF, ON]])
    gosper[6:8, 23:26] = np.array([[ON, OFF, ON],
                                   [OFF, OFF, ON]])

    grid[i:i+11, j:j+38] = gosper
    return grid

def random_grid(N, p):
    grid = np.random.choice(vals, N**2, p=[p, 1-p]).reshape(N, N)
    return grid


def update(frame_num, img, grid, N):
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):
            total = (grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, j]
                     + grid[(i-1)%N, (j+1)%N] + grid[i, (j-1)%N]
                     + grid[i, (j+1)%N] + grid[(i+1)%N, (j-1)%N]
                     + grid[(i+1)%N, j] + grid[(i+1)%N, (j+1)%N])//int(ON)

            if grid[i, j] == ON:
                new_grid[i, j] = OFF if (total < 2) or (total > 3) else ON
            else:
                new_grid[i, j] = ON if total == 3 else OFF

    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img,

def main():
    parser = argparse.ArgumentParser(description="Runs Conways Gmae of Life Simulation.")
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    # parser.add_argument('--glider', dest='glider', required=False)
    parser.add_argument('--demo', dest='demo', required=False)
    args = parser.parse_args()

    # init gridsize and update interval
    N = int(args.N) if args.N and (int(args.N)) > N_min else 100
    update_interval = int(args.interval) if args.interval else 50

    # declare grid
    grid = np.array([])
    # check if glider demo is specified
    if args.demo:
        grid = np.zeros(N**2).reshape(N, N)
        if args.demo == 'glider':
            grid = add_glider(1, 1, grid)
        elif args.demo == 'gosper':
            grid = add_gosper(1, 1, grid)
        else:
            raise ValueError("Invalid option for --demo")
    else:
        p = 0.3
        grid = random_grid(N, p)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames=10,
                                  interval=update_interval,
                                  save_count=50)

    # set the output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=[-'-vcodec', 'libx264'])

    plt.show()
    pass


if __name__ == '__main__':
    main()

