
import argparse
import pprint
from decode import decode
from z80 import Z80


def main():

    rom = None
    cpu = Z80(None)

    def byte(pc):
        return rom[pc]

    def word(pc):
        return rom[pc] | rom[pc + 1] << 8

    parser = argparse.ArgumentParser()
    parser.add_argument('rom', help='the rom file to use')
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

    while True:
        try:
            i = decode(cpu.pc, byte, word)
            cpu.run(i)
        except:
            print('Unhandled instruction')
            pprint.pprint(i)
            break


if __name__ == '__main__':
    main()
