import numpy as np


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
        man = [[ix, iy+5] for ix, iy in zip(x,y)]
        men.append(man)
    return men

def init_onair():
    path_onair = 'animations\\on_air0'
    onair = np.loadtxt(path_onair).tolist()
    x = [int(i) for i in [onair[i][0] for i in range(len(onair))]]
    y = [int(i) for i in [onair[i][1] for i in range(len(onair))]]
    max_x = max(x)
    max_y = max(y)
    onair = [[max_x - ix+ 6, iy] for ix, iy in zip(x,y)]
    return onair

class Animations():
    def __init__(self, size) -> None:
        self.step = 1
        self.size = size
        self.men = init_man()
        self.onair = init_onair()
        self.animations = {'men':'get_man'}
        # men


    def get_onair(self, cnt):
        if cnt%20 == 0:
            self.step = ((self.step+1)%2)
        if self.step == 0:
            return self.on_air
        else:
            return []


    def get_man(self, cnt):
        if cnt%30 == 0:
            self.step = ((self.step+1)%3)
        return self.men[self.step]


    def get_animation(self, cnt, func):
        if func == 'men':
            return self.get_man(cnt)
        if func == 'onair':
            return self.get_onair(cnt)
        else:
            print('prog not available')

         

if __name__ == '__main__':
    animations = Animations()
    print(animations.get_onair(0))
    print(animations.get_man(1))
