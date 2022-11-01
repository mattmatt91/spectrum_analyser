from cProfile import label
from locale import normalize
import numpy as np
import pyaudio as pa
import struct
import matplotlib.pyplot as plt
import time
from math import log10, log
from matrix import Matrix, wheel

TEST = False

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
        self.flag = True

    def check_devices(self):
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ",
                      p.get_device_info_by_host_api_device_index(0, i).get('name'))

    def init_matplot(self):
        plt.ion()
        self.fig, (ax, ax1, ax2, self.ax3) = plt.subplots(4)
        x_fft = np.linspace(0, RATE, CHUNK)
        x = np.arange(0, 2*CHUNK, 2)
        labels_bar = [f'f{i}' for i in range(BANDS)]
        vals_bar = [BANDS for _ in range(BANDS)]
        self.bar = ax2.bar(labels_bar, vals_bar)
        self.line_fft,  = ax1.semilogx(x_fft, np.random.rand(CHUNK), 'r')
        self.line_fft_nonlog,  = self.ax3.plot(np.random.rand(FREQ_AREA), 'r')
        self.line, = ax.plot(x, np.random.rand(CHUNK), 'r')

        ax.set_ylim(-32000, 32000)
        ax.set_xlim = (0, CHUNK)
        ax1.set_xlim(20, RATE/2)
        ax1.set_ylim(0, 1)
        self.fig.show()

    def update_matplot(self, dataInt, dataFFT, mappedFFT):
        self.line.set_ydata(dataInt)
        self.line_fft_nonlog.set_ydata(dataFFT[:FREQ_AREA])
        self.line_fft.set_ydata(dataFFT)
        for bar, val in zip(self.bar, mappedFFT):
            bar.set_height(val)
        stream.fig.canvas.draw()
        stream.fig.canvas.flush_events()

    def get_data(self):
        data = self.stream.read(CHUNK)
        dataInt = struct.unpack(str(CHUNK) + 'h', data)
        dataFFT = np.abs(np.fft.fft(dataInt))*2/(11000*CHUNK)
        return dataInt, dataFFT

    def map_data(self, dataFFT):
        normalised = []
        stops = []
        starts = []
        for band in range(BANDS):
            start = int(WIN_SIZE*band)
            stop = int(WIN_SIZE*(band+1))
            stops.append(stop+SHIFT)
            starts.append(start+SHIFT)
            sub_arr = dataFFT[start:stop]
            val = np.max(sub_arr)
            _val = (1 - log(val + 1, (2.5)))*val*BOOST
            if val >= 1:
                val = 1
            elif val > 0:
                val = 0
            normalised.append(int(_val*(BANDS)))
        if TEST:
            if self.flag:
                self.flag = False
            for bar in stops:
                self.ax3.axvline(x=bar, color='b', label='axvline - full height')
            for bar in starts:
                self.ax3.axvline(x=bar, color='g', label='axvline - full height')
        return normalised

    def draw_matrix(self, mapped_data):
        matrix.clear()
        for y, x in zip(mapped_data, range(BANDS)):
            # print(x, y)
            for i in range(y+1):
                if i == y:
                    matrix.draw(x, i, [255, 255, 0])
                else:
                    matrix.draw(x, i, [255, 0, 0])
        matrix.pixels.show()
        # time.sleep(0.1)


if __name__ == '__main__':
    stream = Stream()
    if TEST:
        stream.init_matplot()
    while True:
        dataInt, dataFFT = stream.get_data()
        fft_mapped = stream.map_data(dataFFT)
        stream.draw_matrix(fft_mapped)
        if TEST:
            stream.update_matplot(dataInt, dataFFT, fft_mapped)
