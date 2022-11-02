from time import sleep
import board
import neopixel_spi as neopixel
from PIL import Image
from adafruit_pixel_framebuf import PixelFramebuffer
from time import sleep
import numpy as np
from numpy import imag
from man import get_men
width = 16
spi = board.SPI()

pixels = neopixel.NeoPixel_SPI(spi,
                                    width*width,
                                    brightness=0.1,
                                    auto_write=False)


pixel_framebuf = PixelFramebuffer(
    pixels,
    width,
    width,
    reverse_x=True,
)
pixel_framebuf.fill(0x0000FF)
pixel_framebuf.pixel(4, 6, 0xFF0000)
pixel_framebuf.hline(2, 3, 5, 0xFF0000)
pixel_framebuf.vline(2, 3, 5, 0xFF0000)
pixel_framebuf.rect(2, 2, 8, 12, 0xFF0000)
pixel_framebuf.fill_rect(4, 4, 8, 12, 0xFF0000)



def map_color(c_rgb): # rgb to hex
    c_hex = "0x"
    for color in c_rgb:
        if len(str(hex(color))) ==3:
            c_hex += "0"
        c_hex += str(hex(color))[2:]
    c_hex = int(c_hex, 16)
    return c_hex


image = Image.new("RGBA", (width, width))
# image.thumbnail((16,16), Image.Resampling.LANCZOS)

# Open the icon
pixel_framebuf.pixel(4, 6, 0xFF0000)

men = get_men()
while True:
        for man in men:
            pixel_framebuf.fill(0x000000)
            pixel_framebuf.fill_rect(4, 0, 12, 9, 0xFF0000)
            for pix in men[0]:
                pixel_framebuf.pixel(pix[0], pix[1], map_color([0,255,0]))
                # print(pix)
            pixel_framebuf.display()
            sleep(1)



