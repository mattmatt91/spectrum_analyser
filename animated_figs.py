import numpy as np
from random import randint


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
        color = [[255,0,0] for _ in range(len(x))]
        man = [[ix, iy+5, c] for ix, iy, c in zip(x,y,color)]
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
                color = wheel(randint(0,255))
                self.buffer.append([x,y, color])

    def get_animation(self, cnt, func):
        if func == 'men':
            return self.get_man(cnt)
        if func == 'onair':
            return self.get_onair(cnt)
        if func == 'random':
            return self.get_random(cnt)
        else:
            print('prog not available')
    
    def get_onair(self, cnt):
        if cnt%20 == 0:
            self.step = ((self.step+1)%2)
        if self.step == 0:
            return self.onair
        else:
            return []
    
    def get_random(self, cnt):
        if cnt%5 == 0:
            self.buffer = []
            for x in range(SIZE):
                for y in range(SIZE):
                    color = [int(i*0.1) for i in wheel((cnt+randint(1,100))%255)]
                    self.buffer.append([x,y, color])
                
        return self.buffer
    
    def get_man(self, cnt):
        if cnt%30 == 0:
            self.step = ((self.step+1)%3)
        return self.men[self.step]



         

if __name__ == '__main__':
    animations = Animations()
    print(animations.get_onair(0))
    print(animations.get_man(1))
