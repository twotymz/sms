import argparse
import os
from dataclasses import dataclass
import decode
import numpy as np


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


def disassembler(path):
    sms = SegaMasterSystem()
    sms.load(path)

    header = sms.readHeader()

    print('=' * 20)
    print(header)
    print('=' * 20)

    sms.load(path)

    byte = lambda a: sms.readByte(a)
    word = lambda a: sms.readWord(a)

    pc = 0
    while pc < sms.bytes:
        decoded = decode.decode(pc, byte, word)

        bytes = 0
        for i in range(decoded.bytes):
            bytes = bytes << 4 * i | sms.readByte(pc + i)

        print(f' {pc:04X}  {bytes:08X}  {decoded.mnemonic}  ({decoded.prefix}, {decoded.displacement}, {decoded.immediate})')
        pc += decoded.bytes


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='the rom file to use')
    args = parser.parse_args()
    disassembler(args.path)
