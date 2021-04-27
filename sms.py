import argparse
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


def sms(path):

    rom = None
    cpu = Z80(None)

    def byte(pc):
        return rom[pc]

    def word(pc):
        return rom[pc] | rom[pc + 1] << 8

    parser = argparse.ArgumentParser()
    parser.add_argument('rom', help='the rom file to use')
    parser.add_argument('--instructions', type=int)
    args = parser.parse_args()

    with open(args.rom, 'rb') as binfile:
        rom = bytearray(binfile.read())

    header = {}
    header['raw'] = ' '.join(['{0:02X}'.format(r) for r in rom[0x7FF0:0x8000]])
    header['tmr_sega'] = ''.join([chr(r) for r in rom[0x7FF0:0x7FF8]])
    header['checksum'] = word(0x7FFA)
    header['product_code'] = word(0x7FFC) | ((byte(0x7FFE) & 0xF0) >> 4) << 16
    header['version'] = byte(0x7FFE) & 0xF
    header['region'] = (byte(0x7FFF) & 0xF0) >> 4
    header['size'] = byte(0x7FFF) & 0xF

    instructions_executed = 0

    while True:
        try:
            i = decode(cpu.pc, byte, word)
            cpu.run(i)
        except:
            print('Unhandled instruction')
            pprint.pprint(i)
            break

        instructions_executed += 1
        if args.instructions and args.instructions == instructions_executed:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='the rom file to use')
    args = parser.parse_args()
    sms(args.path)
