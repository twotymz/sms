import os
from dataclasses import dataclass


@dataclass
class Header:
    raw: str = None
    tmr_sega: str = None
    checksum: int = 0
    product_code: int = 0
    version: int = 0
    region: int = 0
    size: int = 0


class Cartridge:

    def __init__(self):
        self._rom = None

    def load(self, path):
        self._rom = None

        fs = os.path.getsize(path)
        with open(path, 'rb') as fp:
            if fs % 1024:
                fp.seek(512)
                fs -= 512
            self._rom = bytearray(fp.read())

    def readHeader(self):
        """ Read and decode the header from the loaded rom.

        Returns:
            Header: the decoded header object
        """
        header = Header()
        header.raw = ' '.join ([f'{r:02X}' for r in self._rom[0x7FF0:0x8000]])
        header.tmr_sega = ''.join ([chr(r) for r in self._rom[0x7FF0:0x7FF8]])
        header.checksum = self._rom[0x7FFA]
        # TODO product code is wrong
        header.product_code = (self._rom[0x7FFC] << 8 | self._rom[0x7FFD]) | ((self._rom[0x7FFE] & 0xF0) >> 4) << 16
        header.version = self._rom[0x7FFE] & 0xF
        header.region = (self._rom[0x7FFF] & 0xF0) >> 4
        header.size = self._rom[0x7FFF] & 0xF
        return header
