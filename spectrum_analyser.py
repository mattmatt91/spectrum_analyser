from cProfile import label
from locale import normalize
import numpy as np
import pyaudio as pa
import struct
import matplotlib.pyplot as plt
import time
from math import log10, log
from matrix import Matrix, wheel


CHUNK = 1024
FORMAT = pa.paInt16
CHANNELS = 1
RATE = 44100  # in Hz
OFFSET = 80
BANDS = 16
DEVICE_INDEX = 2
FREQ_AREA = 30  # Hz
WIN_SIZE = FREQ_AREA/BANDS
SHIFT = 5
BOOST = 2
SMOOTH = 2  # high value is slow fall
FALLDOWN = 5  # high value is slow fall
FADESPEED = 5  # color change speed, high value is lsow speed
RAINBOW = 3  # 255//BANDS  # gradient of colors for x axis


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

    def render(self, old_values, max_values):
        self.matrix.clear()
        col_val = (self.cnt//FADESPEED)
        for x in range(BANDS):
            col_val += RAINBOW
            for i in range(old_values[x]):
                self.matrix.draw_pixel(x, i, wheel(col_val % 255))
            self.matrix.draw_pixel(x, max_values[x], [125, 125, 0])
        self.cnt += 1


class Visualization():
    def __init__(self):
        self.old_vals = [0 for _ in range(16)]
        self.max_vals = [0 for _ in range(16)]
        self.cnt = 0

    def update_max(self, new_data):
        for new, old, i in zip(new_data, self.max_vals, range(BANDS)):
            if new >= old:
                self.max_vals[i] = new
            else:
                if self.cnt % FALLDOWN == 0:
                    self.max_vals[i] = old - 1 if old > 0 else old

    def update_last(self, new_data):
        for new, old, i in zip(new_data, self.old_vals, range(BANDS)):
            if new >= old:
                self.old_vals[i] = new
            else:
                if self.cnt % SMOOTH == 0:
                    self.old_vals[i] = old - 1 if old > 0 else old

    def update(self, data):
        self.update_max(data)
        self.update_last(data)


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
        self.flag = True  # for test mode

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

    def map_data(self, dataFFT):
        normalised = []
        for band in range(BANDS):
            sub_arr = cut_sub_array(dataFFT, band)
            val = np.max(sub_arr)
            val = (1 - log(val + 1, (2.5)))*val*BOOST
            val = between0and1(val)
            normalised.append(int(val*(BANDS)))

        return normalised


if __name__ == '__main__':
    stream = Stream()
    visualization = Visualization()
    neopixelMatrix = NeoPixelMatrix()

    while True:
        # get data from audio interface
        dataInt, dataFFT = stream.get_data()

        # process data
        data = stream.map_data(dataFFT)

        # update visualization
        visualization.update(data)

        # render to led matrix
        NeoPixelMatrix.render(visualization.old_vals, visualization.max_vals)
