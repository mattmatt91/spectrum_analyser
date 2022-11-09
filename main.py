




def mapping_to_range(val, min_o=0, max_o=1, dtype=float):
    if dtype == bool:
        return bool(round(int(val)/100, 0))
    val = int(val)
    m = (max_o - min_o)/100
    b = min_o
    mapped_value = m * val + b
    return dtype(mapped_value)

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

    def get_data(self):
        data = {'brigthness':self.BRIGHTNESS,
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
        return data
        

    def set_brightness(self, val):
        val = mapping_to_range(val, 0, 0.2, float)
        self.neopixelmatrix.matrix.pixels.brightness = val
        return val

    def set_animation(self, val):
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