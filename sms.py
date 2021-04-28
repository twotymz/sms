import os
import numpy as np
import argparse
from dataclasses import dataclass
from z80 import Z80


@dataclass
class Header:
    raw: str = None
    tmr_sega: str = None
    checksum: int = 0
    product_code: int = 0
    version: int = 0
    region: int = 0
    size: str = None


class SegaMasterSystem:

    def __init__(self):
        self._rom = None
        self._ram = np.

    def load(self, path):
        self._rom = None

        try:

            fs = os.path.getsize(path)
            with open(path, 'rb') as fp:
                if fs % 1024:
                    fp.seek(512)
                    fs -= 512
                self._rom = np.fromfile(fp, dtype=np.uint8)
            return True

        except:
            raise

    @property
    def bytes(self):
        return len(self._rom)

    def readByte(self, addr):
        """ Return the 8-bit value at "addr".

        Args:
            addr (int) -- 16 bit value to read the 8 bit value from

        Returns:
            int: the value read
        """
        return self._rom[addr]

    def readWord(self, addr):
        """ Return a 16-bit value at addr.

        Args:
            addr (int) -- 16 bit address to read the 16 bit value from

        Returns:
            int: the value read
        """
        return self._rom[addr] | self._rom[addr + 1] << 8

    def readHeader(self):
        """ Read and decode the header from the loaded rom.

        Returns:
            Header: the decoded header object
        """
        header = Header()
        header.raw = ' '.join ([f'{r:02X}' for r in self._rom[0x7FF0:0x8000]])
        header.tmr_sega = ''.join ([chr(r) for r in self._rom[0x7FF0:0x7FF8]])
        header.checksum = self.readWord(0x7FFA)
        header.product_code = self.readWord(0x7FFC) | (self.readByte(0x7FFE) & 0xF0 >> 4) << 16
        header.version = self.readByte(0x7FFE) & 0xF
        header.region = self.readByte(0x7FFF) & 0xF0 >> 4
        header.size = self.readByte(0x7FFF) & 0xF
        return header
