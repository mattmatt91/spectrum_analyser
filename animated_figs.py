
import numpy as np


class Animations():
    def __init__(self) -> None:
        self.step = 1
        # men
        path_men = ['animations\\men0', 'animations\\men1', 'animations\\men2']
        men  = [np.loadtxt(man).tolist() for man in path_men]
        self.men = []
        for man in men:
            x = [int(i) for i in [man[i][0] for i in range(len(man))]]
            y = [int(i) for i in [man[i][1] for i in range(len(man))]]

            max_x = max(x)
            max_y = max(y)

            man = [[ix, iy+6] for ix, iy in zip(x,y)]
            self.men.append(man)

        # ON AIR
        path_onair = 'animations\\on_air0'
        self.on_air = np.loadtxt(path_onair)
        self.on_air = self.on_air.tolist()
        x = [int(i) for i in [self.on_air[i][0] for i in range(len(self.on_air))]]
        y = [int(i) for i in [self.on_air[i][1] for i in range(len(self.on_air))]]
        max_x = max(x)
        max_y = max(y)
        self.on_air = [[max_x - ix+ 6, iy] for ix, iy in zip(x,y)]


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

if __name__ == '__main__':
    animations = Animations()
    print(animations.get_onair(0))
    print(animations.get_man(1))
