from functools import cache
import usb
import usb.util
import time
import board
import neopixel_spi as neopixel
import math

dev = usb.core.find(idVendor=0x0403, idProduct=0x6014)
PIXEL_ORDER = neopixel.GRB
COLORS = (0xFF0000, 0x00FF00, 0x0000FF)
DELAY = 0.1
spi = board.SPI()
length = 16


class Matrix():
    def __init__(self):
        self.pixels = neopixel.NeoPixel_SPI(spi,
                                            length*length,
                                            brightness=0.01,
                                            pixel_order=PIXEL_ORDER,
                                            auto_write=False)

    def draw(self, x, y, color):
        if x % 2 == 0:
            index = length * (length-x) - (y+1)
        else:
            index = length * (length-(x+1))+y
        # index = get_index(x,y)
        self.pixels[index] = color

    def clear(self):
        self.pixels.fill(0)


def get_sine(x, freq, amp):
    v = ((math.sin(((time.time())*freq))+1)/2)*x
    v *= amp
    return int(v)


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
        b = 0  # int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return [r, g, b]



def draw_sine(cnt):
    for x in range(length):
        color = wheel(((cnt+length//2)*length) % 255)
        ymax = get_sine(length, 32, 0.5) + length//3
        for y in range(ymax):
            matrix.draw(x, y, color)
        for y in range(length-ymax):
            matrix.draw(x, y+ymax, color)
        matrix.draw(x, ymax, wheel((cnt+length) % 255))
        matrix.pixels.show()


if __name__ == '__main__':
    matrix = Matrix()

    cnt = 0
    while True:
        # matrix.clear()
        draw_sine(cnt)
        cnt += 1
