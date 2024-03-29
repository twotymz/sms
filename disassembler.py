import argparse
import decode
from memory import Memory
from cartridge import Cartridge


def disassembler(path):
    cart = Cartridge()
    memory = Memory()

    cart.load(path)
    header = cart.read_header()
    memory.load_cart(cart)

    print('=' * 20)
    print(header)
    print(f'Num pages: {cart.pages}')
    print('=' * 20)

    pc = 0
    while pc < 0xFFFF:

        decoded = decode.decode(pc, memory)
        bytes = ''
        for i in range(decoded.bytes):
            bytes += f'{memory.read(pc + i):02X}'

        while len(bytes) < 6:
            bytes = '00' + bytes

        print(f' {pc:04X}  0x{bytes}  {decoded.mnemonic}  ({decoded.prefix << 8|decoded.opcode:06X}, {decoded.displacement:04X}, {decoded.immediate:04X})')
        pc += decoded.bytes


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='the rom file to use')
    args = parser.parse_args()
    disassembler(args.path)
