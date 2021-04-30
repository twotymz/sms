from z80 import Z80
from cartridge import Cartridge
from memory import Memory
from decode import decode
from instructions import instructions

cartridge = Cartridge()
memory = Memory()
cpu = Z80()

cartridge.load('roms/transbot.sms')
memory.loadCart(cartridge)

while True:
    print(cpu)

    decoded = decode(cpu.pc.reg, memory)
    print(f'\n {decoded.mnemonic}')
    print('-' * 95)

    cpu.pc.reg += decoded.bytes
    try:
        cycles = instructions[decoded.instruction](decoded, cpu, memory)
    except KeyError:
        print(f'Unhandled instruction 0x{decoded.instruction:06X}')
        exit()
