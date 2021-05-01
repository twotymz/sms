from dataclasses import dataclass


@dataclass
class Noise:
    reg: int = 0

    def write(self, data):
        # TODO...
        self.reg = data & 0x7


@dataclass
class Tone:
    reg: int = 0

    def write(self, data):
        pass


@dataclass
class Volume:
    reg: int = 0xF

    def write(self, data):
        pass


class PSG:

    def __init__(self):
        self._channels = [
            (Volume(), Tone()),
            (Volume(), Tone()),
            (Volume(), Tone()),
            (Volume(), Noise())
        ]


    def write(self, byte):
        if byte & 0x7:
            # Latch/data byte
            channel = (byte & 0x60) >> 5
            type = (byte & 0x10) >> 4
            data = byte & 0xF

            volume, tone = self._channels[channel]
            if type:
                volume.write(data)
            else:
                tone.write(data)

        else:
            # data byte
            data = byte & 0x3F
