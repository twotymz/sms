from dataclasses import dataclass


@dataclass
class Noise:
    reg: int = 0        # 3 bits of noise info

    def latched(self, data):
        self.reg = self.reg & 0x7

    def write(self, data):
        self.reg = self.reg & 0x7


@dataclass
class Tone:
    reg: int = 0        # 10 bit of tone info

    def latched(self, data):
        self.reg = data & 0xF

    def write(self, data):
        self.reg = (self.reg | (data << 6)) & 0x3FF


@dataclass
class Volume:
    reg: int = 0xF      # 4 bits of attenuation, 0x0 = full, 0xF = silence

    def write(self, data):
        self.reg = data & 0xF


class PSG:

    def __init__(self):

        self._channels = [
            (Volume(), Tone()),
            (Volume(), Tone()),
            (Volume(), Tone()),
            (Volume(), Noise())
        ]

        self._latched = None

    def write(self, byte):
        if byte & 0x7:
            # Latch/data byte
            channel = (byte & 0x60) >> 5
            type = (byte & 0x10) >> 4
            data = byte & 0xF

            volume, tone = self._channels[channel]
            if type:
                self._latched = volume
            else:
                self._latched = tone

            self._latched.write(data)

        else:
