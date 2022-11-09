
import numpy as np
import pyaudio as pa
import struct
from math import log
from matrix import Matrix, wheel
from animated_figs import Animations

CHUNK = 1024  # audio resolution
FORMAT = pa.paInt16
CHANNELS = 1
RATE = 44100  # in Hz
BANDS = 16  # number of pixel cols
DEVICE_INDEX = 2  # audio interface

BRIGHTNESS = 0.1
FREQAREA = 20  # win size of raw data --> change in UI
WINSIZE = FREQAREA/BANDS  # size of array for one band at matrix
SMOOTH = 3  # high value is slow fall --> change in UI
FALLDOWN = 7  # high value is slow fall --> change in UI
FADESPEED = 10  # color change speed, high value is lsow speed --> change in UI
RAINBOW = 10  # 255//BANDS  # gradient of colors for x axis --> change in UI
YRAINBOW = 20  # 255//BANDS  # gradient of colors for y axis --> change in UI
SYM = False  # --> change in UI
MAXDOT = True  # draw max dot  --> change in UI
BLACKSPEC = False  # --> change in UI
CENTER = True  # when sym is true, drw center or borders --> change in UI


def between0and1(val):
    if val >= 1:
        return 1
    elif val < 0:
        return 0
    else:
        return val


def cut_sub_array(dataFFT, band):
    start = int(Frame.WINSIZE*band)
    stop = int(Frame.WINSIZE*(band+1))
    sub_arr = dataFFT[start:stop]
    return sub_arr

# mapping values between 0 and 100 to range


def mapping_to_range(val, min_o=0, max_o=1, dtype=float):
    if dtype == bool:
        return bool(round(int(val)/100, 0))
    val = int(val)
    m = (max_o - min_o)/100
    b = min_o
    mapped_value = m * val + b
    return dtype(mapped_value)


class NeoPixelMatrix:
    def __init__(self):
        self.matrix = Matrix()
        self.cnt = 0

    def render_spec(self, old_values, max_values):
        col_val = (self.cnt//Frame.FADESPEED)
        for x in range(BANDS):
            col_val += Frame.RAINBOW
            if Frame.SYM:
                for i in range(old_values[x]//2):
                    color = [0, 0, 0] if Frame.BLACKSPEC else wheel(
                        (col_val+Frame.YRAINBOW*i) % 255)
                    if Frame.CENTER:
                        self.matrix.draw_pixel(
                            x, i+BANDS//2-1, color, invert=True, rot_y=True)
                        self.matrix.draw_pixel(
                            x, BANDS//2-i, color, invert=True, rot_y=True)
                    else:
                        self.matrix.draw_pixel(
                            x, i, color, invert=True, rot_y=True)
                        self.matrix.draw_pixel(
                            x, BANDS-i-1, color, invert=True, rot_y=True)
                if Frame.MAXDOT:
                    if Frame.CENTER:
                        self.matrix.draw_pixel(
                            x, max_values[x]//2+BANDS//2-1, [255, 0, 0], invert=True, rot_y=True)
                        self.matrix.draw_pixel(
                            x, BANDS//2-max_values[x]//2, [255, 0, 0], invert=True, rot_y=True)
                    else:
                        self.matrix.draw_pixel(
                            x, max_values[x]//2, [255, 0, 0], invert=True, rot_y=True)
                        self.matrix.draw_pixel(
                            x, BANDS-max_values[x]//2 - 1, [255, 0, 0], invert=True, rot_y=True)

            if not Frame.SYM:
                for i in range(old_values[x]):
                    color = [0, 0, 0] if Frame.BLACKSPEC else wheel(
                        (col_val + Frame.YRAINBOW*i) % 255)
                    self.matrix.draw_pixel(x, i, color, rot_x=True, rot_y=True)
                if Frame.MAXDOT:
                    self.matrix.draw_pixel(
                        x, max_values[x], [255, 0, 0], rot_x=True, rot_y=True)

    def show(self):
        self.cnt += 1
        self.matrix.show()

    def clear(self):
        self.matrix.clear()

    def render_animation(self, dots):
        if dots != None:
            for dot in dots:
                self.matrix.draw_pixel(int(dot[0]), int(
                    dot[1]), dot[2], rot_x=True, rot_y=True)


class Visualization():
    def __init__(self):
        self.old_vals = [0 for _ in range(16)]
        self.max_vals = [0 for _ in range(16)]

    def update_max(self, cnt, new_data):
        for new, old, i in zip(new_data, self.max_vals, range(BANDS)):
            if new >= old:
                self.max_vals[i] = new
            else:
                if cnt % Frame.FALLDOWN == 0:
                    self.max_vals[i] = old - 1 if old > 0 else old

    def update_last(self, cnt,  new_data):
        for new, old, i in zip(new_data, self.old_vals, range(BANDS)):
            if new >= old:
                self.old_vals[i] = new
            else:
                if cnt % Frame.SMOOTH == 0:
                    self.old_vals[i] = old - 1 if old > 0 else old

    def update(self, cnt, data):
        self.update_max(cnt, data)
        self.update_last(cnt, data)


class Stream(object):
    def __init__(self):
        self.p = pa.PyAudio()
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK  # ,
            # input_device_index=DEVICE_INDEX
        )
        self.check_devices()
        self.max_val = 0

    def check_devices(self):
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ",
                      self.p.get_device_info_by_host_api_device_index(0, i).get('name'))

    def get_data(self):
        data = self.stream.read(CHUNK)
        dataInt = struct.unpack(str(CHUNK) + 'h', data)
        dataFFT = np.abs(np.fft.fft(dataInt))*2/(11000*CHUNK)
        return dataInt, dataFFT

    def map_ln(self, val):
        val = 0 if val <= 0 else val
        if val == 0:
            return 0
        val = (log(val)+4)/4
        return val

    def map_data(self, dataFFT):
        normalised = []
        for band in range(BANDS):
            sub_arr = cut_sub_array(dataFFT, band)
            val = np.max(sub_arr)
            if val > self.max_val:
                self.max_val = val
            val = val/self.max_val
            val = self.map_ln(val)  # fit to signal
            normalised.append(int(val*(BANDS)))
        return normalised


class Frame():
    BRIGHTNESS = BRIGHTNESS
    FREQAREA = FREQAREA
    WINSIZE = WINSIZE
    SMOOTH = SMOOTH
    FALLDOWN = FALLDOWN
    FADESPEED = FADESPEED
    RAINBOW = RAINBOW
    YRAINBOW = YRAINBOW
    SYM = SYM
    MAXDOT = MAXDOT
    BLACKSPEC = BLACKSPEC
    CENTER = CENTER


    def __init__(self) -> None:
        self.stream = Stream()
        self.visualization = Visualization()
        self.neopixelmatrix = NeoPixelMatrix()
        self.animations = Animations()
        self.animations_list = self.animations.get_list()
        self.animation = 'moodulo'
        self.render_spec = True
        self.render_animation = False

        self.data = {'brigthness':self.BRIGHTNESS,
                'freqarea':self.FREQAREA,
                'smooth':self.SMOOTH,
                'falldown':self.FALLDOWN,
                'fadespeed':self.FADESPEED,
                'rainbow':self.RAINBOW,
                'yrainbow':self.YRAINBOW,
                'sym':self.SYM,
                'maxdot':self.MAXDOT,
                'blackspec':self.BLACKSPEC,
                'center': self.CENTER,
                'animation':self.animation,
                'render_spec':self.render_spec,
                'render_animation':self.render_animation}

        self.setter = {'brigthness':self.set_brightness,
                'freqarea':self.set_freqarea,
                'smooth':self.set_smooth,
                'falldown':self.set_falldown,
                'fadespeed':self.set_fadespeed,
                'rainbow':self.set_rainbow,
                'yrainbow':self.set_yrainbow,
                'sym':self.set_sym,
                'maxdot':self.set_maxdot,
                'blackspec':self.set_blackspec,
                'center': self.set_center,
                'animation':self.set_animation,
                'render_spec':self.set_render_spec,
                'render_animation':self.set_render_animation}

    def get_data(self):
        return self.data
        
    def set_feature(self, feature, val):
        val = self.setter[feature](val)
        return val

    def set_brightness(self, val):
        val = mapping_to_range(val, 0, 0.2, float)
        self.neopixelmatrix.matrix.pixels.brightness = val
        return val

    def set_animation(self, val):
        print('test')
        val = mapping_to_range(val, 0, len(self.animations_list), int)
        self.animation = self.animations_list[val-1]
        print(self.animation)
        return self.animation
    
    def set_render_spec(self, val):
        val = mapping_to_range(val, 0, 1, bool)
        self.render_spec = val
        return val
    
    def set_render_animation(self, val):
        val = mapping_to_range(val, 0, 1, bool)
        self.render_animation = val
        return val

    @classmethod
    def set_freqarea(cls, val):
        val = mapping_to_range(val, BANDS, 100, int)
        cls.FREQAREA = val
        cls.WINSIZE = Frame.FREQAREA/BANDS
        return val

    @classmethod
    def set_smooth(cls, val):
        val = mapping_to_range(val, 1, 10, int)
        cls.SMOOTH = val
        return val

    @classmethod
    def set_falldown(cls, val):
        val = mapping_to_range(val, cls.SMOOTH, 15, int)
        cls.FALLDOWN = val
        return val

    @classmethod
    def set_fadespeed(cls, val):
        val = mapping_to_range(val, 1, 20, int)
        cls.FADESPEED = val
        return val

    @classmethod
    def set_rainbow(cls, val):
        val = mapping_to_range(val, 0, 30, int)
        cls.RAINBOW = val
        return val

    @classmethod
    def set_yrainbow(cls, val):
        val = mapping_to_range(val, 0, 30, int)
        cls.YRAINBOW = val
        return val

    @classmethod
    def set_sym(cls, val):
        val = mapping_to_range(val, 0, 1, bool)
        cls.SYM = val
        return val

    @classmethod
    def set_maxdot(cls, val):
        val = mapping_to_range(val, 0, 1, bool)
        cls.MAXDOT = val
        return val

    @classmethod
    def set_blackspec(cls, val):
        val = mapping_to_range(val, 0, 1, bool)
        cls.BLACKSPEC = val
        return val

    @classmethod
    def set_center(cls, val):
        val = mapping_to_range(val, 0, 1, bool)
        cls.CENTER = val
        return val

    def update(self):
        while True:
            # get data from audio interface
            dataInt, dataFFT = self.stream.get_data()

            # process data
            data = self.stream.map_data(dataFFT)

            # update visualization
            self.visualization.update(self.neopixelmatrix.cnt, data)

            # render to led matrix
            self.neopixelmatrix.clear()
            # render animation
            if self.render_animation:
                self.neopixelmatrix.render_animation(
                    self.animations.get_animation(func=self.animation, beat=data[2]))
            # render spec
            if self.render_spec:
                self.neopixelmatrix.render_spec(
                    self.visualization.old_vals, self.visualization.max_vals)
            self.neopixelmatrix.show()


if __name__ == '__main__':
    frame = Frame()
    frame.update()
