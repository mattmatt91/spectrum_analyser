from functools import cache
from turtle import width
import usb
import usb.util
import time
import board
import neopixel_spi as neopixel
import math
from adafruit_pixel_framebuf import PixelFramebuffer
from PIL import Image
from animated_figs import Animations

dev = usb.core.find(idVendor=0x0403, idProduct=0x6014)
PIXEL_ORDER = neopixel.GRB
COLORS = (0xFF0000, 0x00FF00, 0x0000FF)
DELAY = 0.1
spi = board.SPI()
BANDS = 16


class Matrix():
    def __init__(self):
        self.pixels = neopixel.NeoPixel_SPI(spi,
                                            BANDS*BANDS,
                                            brightness=0.1,
                                            pixel_order=PIXEL_ORDER,
                                            auto_write=False)
        self.pixel_framebuf = PixelFramebuffer(
                                            self.pixels,
                                            BANDS,
                                            BANDS,
                                            reverse_x=False,)


    def draw_pixel(self, x, y, color):
        self.pixel_framebuf.pixel(x, y, self.map_color(color))

    def draw_fill(self, color):
        self.pixel_framebuf.fill(self.map_color(color))

    def draw_line(self, x1, y1, x2, y2, color):
        self.pixel_framebuf.line(x1, y1, x2, y2, self.map_color(color))

    def draw_hline(self, x, y1, y2, color):
        self.pixel_framebuf.hline(x, y1, y2, self.map_color(color))

    def draw_vline(self, y, x1, x2, color):
        self.pixel_framebuf.vline(y, x1, x2, self.map_color(color))

    def draw_rect(self, y, x1, x2, color):
        self.pixel_framebuf.rect(y, x1, x2, self.map_color(color))

    def draw_rect_fill(self, x1, y1, x2, y2, color):
        self.pixel_framebuf.fill_rect(x1, y1, x2, y2, self.map_color(color))

    def show(self):
        self.pixel_framebuf.display()

    def clear(self):
        self.draw_fill([0, 0, 0])

    def draw_text(self, text, x, y, color):
        self.pixel_framebuf.text(text, x, y, self.map_color(color), size=1)

    def map_color(self, c_rgb):  # rgb to hex
        c_hex = '0x'
        for color in c_rgb:
            if len(str(hex(color))) == 3:
                c_hex += '0'
            c_hex += str(hex(color))[2:]
        c_hex = int(c_hex, 16)
        return c_hex


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


if __name__ == '__main__':
    matrix = Matrix()

    cnt = 0
    while True:
        time.sleep(0.1)
        matrix.clear()
        matrix.draw_pixel(cnt%5, cnt%9, [0,0,255])
        matrix.show()
        cnt += 1
