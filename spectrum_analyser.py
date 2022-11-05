
import numpy as np
import pyaudio as pa
import struct
from math import log
from matrix import Matrix, wheel
from animated_figs import Animations

CHUNK = 1024 # audio resolution
FORMAT = pa.paInt16
CHANNELS = 1
RATE = 44100  # in Hz
BANDS = 16 # number of pixel cols
DEVICE_INDEX = 2 # audio interface

BRIGHTNESS = 0.1
FREQ_AREA = 20  # win size of raw data --> change in UI
WIN_SIZE = FREQ_AREA/BANDS # size of array for one band at matrix
SMOOTH = 3  # high value is slow fall --> change in UI
FALLDOWN = 7  # high value is slow fall --> change in UI
FADESPEED = 5  # color change speed, high value is lsow speed --> change in UI
RAINBOW = 4  # 255//BANDS  # gradient of colors for x axis --> change in UI
YRAINBOW = 20 # 255//BANDS  # gradient of colors for y axis --> change in UI
SYM = True # --> change in UI
MAXDOT = True# draw max dot  --> change in UI
BLACKSPEC = False # --> change in UI
CENTER = False # when sym is true, drw center or borders --> change in UI


def between0and1(val):
    if val >= 1:
        return 1
    elif val < 0:
        return 0
    else:
        return val


def cut_sub_array(dataFFT, band):
    start = int(WIN_SIZE*band)
    stop = int(WIN_SIZE*(band+1))
    sub_arr = dataFFT[start:stop]
    return sub_arr


class NeoPixelMatrix:
    def __init__(self):
        self.matrix = Matrix()
        self.cnt = 0

    def render_spec(self, old_values, max_values):
        col_val = (self.cnt//FADESPEED)
        for x in range(BANDS):
            col_val += RAINBOW
            if SYM:   
                for i in range(old_values[x]//2):
                    color = [0,0,0] if BLACKSPEC else wheel((col_val+YRAINBOW*i) % 255)
                    if CENTER:
                        self.matrix.draw_pixel(x, i+BANDS//2-1, color, invert=True, rot_y=True)
                        self.matrix.draw_pixel(x, BANDS//2-i, color, invert=True, rot_y=True)
                    else:
                        self.matrix.draw_pixel(x, i, color, invert=True, rot_y=True)
                        self.matrix.draw_pixel(x, BANDS-i-1, color, invert=True, rot_y=True)
                if MAXDOT:
                    if CENTER:
                        self.matrix.draw_pixel(x, max_values[x]//2+BANDS//2-1, [255, 0, 0], invert=True, rot_y=True)
                        self.matrix.draw_pixel(x, BANDS//2-max_values[x]//2, [255, 0, 0], invert=True, rot_y=True)
                    else:
                        self.matrix.draw_pixel(x, max_values[x]//2, [255, 0, 0], invert=True, rot_y=True)
                        self.matrix.draw_pixel(x, BANDS-max_values[x]//2 -1, [255, 0, 0], invert=True, rot_y=True)

            if not SYM:
                for i in range(old_values[x]):
                    color = [0,0,0] if BLACKSPEC else wheel((col_val+ YRAINBOW*i)% 255) 
                    self.matrix.draw_pixel(x, i, color , rot_x=True, rot_y=True)
                if MAXDOT:
                    self.matrix.draw_pixel(x, max_values[x], [255, 0, 0], rot_x=True, rot_y=True)



    def show(self):
        self.cnt += 1
        self.matrix.show()

    def clear(self):
        self.matrix.clear()


    def render_animation(self, dots):
        for dot in dots:
            self.matrix.draw_pixel(int(dot[0]), int(dot[1]), dot[2], rot_x=True, rot_y=True)
        



class Visualization():
    def __init__(self):
        self.old_vals = [0 for _ in range(16)]
        self.max_vals = [0 for _ in range(16)]

    def update_max(self,cnt, new_data):
        for new, old, i in zip(new_data, self.max_vals, range(BANDS)):
            if new >= old:
                self.max_vals[i] = new
            else:
                if cnt % FALLDOWN == 0:
                    self.max_vals[i] = old - 1 if old > 0 else old

    def update_last(self, cnt,  new_data):
        for new, old, i in zip(new_data, self.old_vals, range(BANDS)):
            if new >= old:
                self.old_vals[i] = new
            else:
                if cnt % SMOOTH == 0:
                    self.old_vals[i] = old - 1 if old > 0 else old

    def update(self,cnt, data):
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
            val = self.map_ln(val) # fit to signal
            normalised.append(int(val*(BANDS)))
        return normalised



class Frame():
    def __init__(self) -> None:
        self.stream = Stream()
        self.visualization = Visualization()
        self.neopixelmatrix = NeoPixelMatrix()
        self.animations = Animations()

    def set_brightness(self, val):
        print(val)
        val = int(val)/100
        print(val)

        self.neopixelmatrix.matrix.pixels.brightness  = val
    


    def set_freq_area(self, val):
        # val = 
        global FREQ_AREA
        FREQ_AREA = val 
        global WIN_SIZE
        WIN_SIZE = FREQ_AREA/BANDS 
    
    def set_smooth(self, val):
        global SMOOTH 
        SMOOTH = val 

    def set_falldown(self, val):
        global FALLDOWN
        FALLDOWN = val 
        
    def set_fadespeed(self, val):
        global FADESPEED
        FADESPEED = val
         
    def set_rainbow(self, val):
        global RAINBOW
        RAINBOW = val
    
    def set_yrainbow(self, val):
        global YRAINBOW
        YRAINBOW = val
    
    def set_sym(self, val):
        global SYM
        SYM = val
    
    def set_maxdot(self, val):
        global MAXDOT
        MAXDOT = val
    
    def set_blackspec(self, val):
        global BLACKSPEC
        BLACKSPEC = val

    def set_center(self, val):
        global CENTER 
        CENTER = val


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
            # self.neopixelmatrix.render_animation(self.animations.get_animation(func='onair', beat=data[2]))
            # self.neopixelmatrix.render_animation(self.animations.get_animation(func='random', beat=data[1]))
            # self.neopixelmatrix.render_animation(self.animations.get_animation( func='men', beat=data[0]))
            self.neopixelmatrix.render_spec(self.visualization.old_vals, self.visualization.max_vals)
            self.neopixelmatrix.show()

if __name__ == '__main__':
    frame = Frame()
    frame.update()
