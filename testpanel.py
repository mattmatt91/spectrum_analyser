import numpy as np
from matplotlib import pyplot as plt
import random
import time

SIZE = 16

class TestPixel():
    def __init__(self, size):
        plt.ion()
        self.fig, (ax) = plt.subplots(1)
        x = [i for i in range(size)]
        y = [i for i in range(size)]
        self.scatter_plot = ax.scatter(x, y)
        for i in range(size):
            ax.axvline(x=i, color='g',
                       label='axvline - full height')
            ax.axhline(y=i, color='g',
                       label='axvline - full height')
        ax.set_ylim(-0.5, size-0.5)
        ax.set_xlim(-0.5, size-0.5)
        self.fig.show()

    def draw(self, x, y, color= [255,255,255]):
        self.scatter_plot.set_offsets(np.c_[x, y])
        self.fig.canvas.flush_events()
        time.sleep(0.1)

if __name__ == '__main__':
    cnt = 0
    testpixel = TestPixel(SIZE)
    while True:
        cnt += 1
        y = [random.randint(0, cnt % SIZE) for _ in range(SIZE)]
        x = [random.randint(0, cnt % SIZE) for _ in range(SIZE)]
        testpixel.draw(x, y)
