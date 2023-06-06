import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import matplotlib.animation as animation

import numpy as np

def time_test(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        output = func(*args, **kwargs)
        print(f'{func} took: {time.time()-start}')
        return output
    return wrapper

def composite(func, grid, repetitions: int, constant: complex):
    current_grid = grid
    track = np.ones(grid.shape)
    one = np.ones(grid.shape)
    for rep in range(repetitions):
        current_grid = func(current_grid, constant)
        one[abs(current_grid)>4] = 0
        track += one
    return track

def sequence(z: complex, constant: complex) -> complex:
    '''Defines the fractal, this is the sequence for the julia-set'''
    return z**2 + constant

def makeGrid(width, height, center, scale):
    x = np.arange(int(center[0]-width//2), int(center[0]+width//2)) * (1+0j)*scale
    y = np.arange(int(center[1]-height//2), int(center[1]+height//2)) * (0+1j)*scale
    real, imag = np.meshgrid(x, y)
    grid = real + imag
    return grid

def generate(width, height, center, scale, repetitions, constant, grid = True):
    if center == (0, 0):
        if grid:
            grid = makeGrid(width, height//2, (0, height//4), scale)

        compose = composite(sequence, grid, repetitions, constant)
        return np.vstack([np.flip(compose, [1,0]), compose])
    if grid:
        grid = makeGrid(width, height, center, scale)
    compose = composite(sequence, grid, repetitions, constant)
    return compose



def generate_video(img):
    frames = [] # for storing the generated images
    fig = plt.figure()
    for i in range(6):
        frames.append([plt.imshow(img[i], cmap= mpl.colormaps["cubehelix"],animated=True)])
    ani = animation.ArtistAnimation(fig, frames, interval=50, blit=True, repeat_delay=1000)
    ani.save('Julie_NEW.mp4')


if __name__ == '__main__':
    plt.imshow(generate(800, 800, (0, 0), 1/400, 500, -0.8 +0.156j), cmap= mpl.colormaps["cubehelix"])
    plt.show()