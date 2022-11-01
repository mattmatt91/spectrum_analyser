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
FADESPEED = 5 # color change speed, high value is lsow speed


p = pa.PyAudio()
matrix = Matrix()


class Stream(object):
    def __init__(self):
        self.stream = p.open(
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
        self.old_vals = [0 for _ in range(16)]
        self.max_vals = [0 for _ in range(16)]
        self.cnt = 0

    def check_devices(self):
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ",
                      p.get_device_info_by_host_api_device_index(0, i).get('name'))

    def get_data(self):
        data = self.stream.read(CHUNK)
        dataInt = struct.unpack(str(CHUNK) + 'h', data)
        dataFFT = np.abs(np.fft.fft(dataInt))*2/(11000*CHUNK)
        return dataInt, dataFFT

    def cut_sub_array(self, dataFFT, band):
        start = int(WIN_SIZE*band)
        stop = int(WIN_SIZE*(band+1))
        sub_arr = dataFFT[start:stop]
        return sub_arr

    def between0and1(self, val):
        if val >= 1:
            return 1
        elif val < 0:
            return 0
        else:
            return val

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

    def map_data(self, dataFFT):
        normalised = []
        for band in range(BANDS):
            sub_arr = self.cut_sub_array(dataFFT, band)
            val = np.max(sub_arr)
            val = (1 - log(val + 1, (2.5)))*val*BOOST
            val = self.between0and1(val)
            normalised.append(int(val*(BANDS)))
        self.update_max(normalised)
        self.update_last(normalised)
        return normalised

    def draw_matrix(self):
        matrix.clear()
        for x in range(BANDS):
            for i in range(self.old_vals[x]):
                matrix.draw(x, i, wheel((self.cnt//FADESPEED)%255))
            matrix.draw(x, self.max_vals[x], [125, 125, 0])
        matrix.pixels.show()
        self.cnt += 1


if __name__ == '__main__':
    stream = Stream()

    while True:
        dataInt, dataFFT = stream.get_data()
        stream.map_data(dataFFT)
        stream.draw_matrix()
