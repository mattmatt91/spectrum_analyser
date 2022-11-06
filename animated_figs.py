import numpy as np
from random import randint
from time import time


SIZE = 16


def init_man():
    path_men = ['animations\\men0', 'animations\\men1', 'animations\\men2']
    arr_men  = [np.loadtxt(man).tolist() for man in path_men]
    men = []
    for man in arr_men:
        x = [int(i) for i in [man[i][0] for i in range(len(man))]]
        y = [int(i) for i in [man[i][1] for i in range(len(man))]]
        max_x = max(x)
        max_y = max(y)
        color = [[0,255,0] for _ in range(len(x))]
        man = [[ix-4, iy+5, c] for ix, iy, c in zip(x,y,color)]
        men.append(man)
    return men

def init_onair():
    path_onair = 'animations\\on_air0'
    onair = np.loadtxt(path_onair).tolist()
    x = [int(i) for i in [onair[i][0] for i in range(len(onair))]]
    y = [int(i) for i in [onair[i][1] for i in range(len(onair))]]
    color = [[255,0,0] for _ in range(len(x))]
    max_x = max(x)
    max_y = max(y)
    onair = [[max_x - ix+ 6, iy, c] for ix, iy, c in zip(x,y,color)]
    return onair

def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return [r, g, b]

class Animations():
    def __init__(self) -> None:
        self.step = 1
        self.men = init_man()
        self.onair = init_onair()

        self.buffer = []
        for x in range(SIZE):
            for y in range(SIZE):
                color = [int(0.1 * i) for i in wheel(randint(0,255))]
                self.buffer.append([x,y, color])

        self.beat_detect = True
        self.last_beat = time()
        self.cnt = 0

    def update_beat_cnt(self, beat):
        self.cnt += 1
        if not self.beat_detect and beat > SIZE//2 and self.last_beat + 0.4 < time():
            self.beat_detect = True
            self.last_beat = time()
            self.step += 1
        elif  self.beat_detect and beat < SIZE//2:
            self.beat_detect = False

    def get_animation(self, func, beat):
        self.update_beat_cnt(beat)
        if func == 'random':
            return self.get_random()
        if func == 'men':
            return self.get_man()
        if func == 'onair':
            return self.get_onair()
        if func == 'modulo':
            return  self.get_modulo()
        else:
            print('prog not available')

    def get_random(self):
        if self.cnt%3== 0:
            self.buffer = []
            for x in range(SIZE):
                for y in range(SIZE):
                    color = [int(i*0.15) for i in wheel((self.cnt+randint(1,100))%255)]
                    self.buffer.append([x,y, color])

        return self.buffer

    def get_modulo(self):
        dots = []
        for x in range(SIZE):
            for y in range(SIZE):
                color = [((self.cnt)//20*(y+1)*(x+1))%255,0,0] # wheel((self.cnt*(y+1)*(x+1))%50)
                dots.append([x,y, color])
        return dots
    
    def get_onair(self):
        if self.step%2 == 0:
            return self.onair
        else:
            return []
    
    
    def get_man(self):
        return self.men[self.step%3]



         

if __name__ == '__main__':
    animations = Animations()
    print(animations.get_onair(0))
    print(animations.get_man(1))
