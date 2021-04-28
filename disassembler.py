import argparse
import decode
from sms import SegaMasterSystem


def disassembler(path):
    sms = SegaMasterSystem()
    sms.load(path)

    header = sms.readHeader()

    print('=' * 20)
    print(header)
    print('=' * 20)

    byte = lambda a: sms.readByte(a)
    word = lambda a: sms.readWord(a)

    pc = 0
    while pc < sms.bytes:

        decoded = decode.decode(pc, byte, word)
        bytes = ''
        for i in range(decoded.bytes):
            bytes += f'{sms.readByte(pc + i):02X}'

        while len(bytes) < 6:
            bytes = '00' + bytes

        print(f' {pc:04X}  0x{bytes}  {decoded.mnemonic}  ({decoded.prefix << 8|decoded.opcode:06X}, {decoded.displacement:04X}, {decoded.immediate:04X})')
        pc += decoded.bytes


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='the rom file to use')
    args = parser.parse_args()
    disassembler(args.path)
