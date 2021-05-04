
class Noise:

    def __init__(self, tone_2):
        self._reg = 0        # 3-bit noise info
        self._counter = 0    # 10-bit counter
        self._tone_2 = tone_2

    def latched(self, data):
        self._reg = data & 0x7

    def write(self, data):
        self._reg = data & 0x7

    def run(self, cycles):

        if self._counter:
            self._counter -= cycles

            if self._counter <= 0:
                two_bits = self._reg & 0x3
                if two_bits == 0x0:
                    self._counter = 0x10
                elif two_bits == 0x1:
                    self._counter = 0x20
                elif two_bits == 0x2:
                    self._counter = 0x40
                elif two_bits == 0x3:
                    self._counter = self._tone_2.counter


class Tone:

    def __init__(self):
        self._reg = 0       # 10-bit tone info
        self._counter = 0   # 10-bit counter
        self._output = 0

    def latched(self, data):
        self._reg = data & 0xF

    def write(self, data):
        self._reg = ((data & 0x3F) << 4) | (self._reg & 0xF)
        self._counter = self._reg

    def run(self, cycles):
        if self._counter:
            self._counter -= cycles

            if self._counter <= 0:
                self._counter += self._reg
                self._output = not self._output


class Volume:

    def __init__(self):
        self._reg = 0xF      # 4-bits of attenuation, 0x0 = full, 0xF = silence

    @property
    def register(self):
        return self._reg

    def latched(self, data):
        self._reg = data & 0xF

    def write(self, data):
        self._reg = data & 0xF


class Channel:

    def __init__(self, volume, tone_noise):
        self._pair = (volume, tone_noise)

    @property
    def pair(self):
        return self._pair

    @property
    def volume(self):
        return self._pair[0]

    @property
    def tone_noise(self):
        return self._pair[1]


class PSG:

    def __init__(self):

        tone_2 = Tone()

        self._channels = [
            Channel(Volume(), Tone()),
            Channel(Volume(), Tone()),
            Channel(Volume(), tone_2),
            Channel(Volume(), Noise(tone_2))
        ]

        self._latched_register = None

    def get_channel(self, c):
        return self._channels[c]

    def run(self, cycles):
        self._channels[0].tone_noise.run(cycles)
        self._channels[1].tone_noise.run(cycles)
        self._channels[2].tone_noise.run(cycles)
        self._channels[3].tone_noise.run(cycles)

    def write(self, byte):
        if byte & 0x80:
            # Latch/data byte
            channel = (byte & 0x60) >> 5
            type = (byte & 0x10) >> 4

            if type:
                self._latched_register = self._channels[channel].volume
            else:
                self._latched_register = self._channels[channel].tone_noise

            self._latched_register.latched(byte & 0xF)

        else:
            # Data byte
            self._latched_register.write(byte & 0x3F)
