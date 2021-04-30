from z80 import Z80
from cartridge import Cartridge
from memory import Memory
from port_mapper import PortMapper
from decode import decode
from instructions import instructions


cartridge = Cartridge()
memory = Memory()
cpu = Z80()
ports = PortMapper()

cartridge.load('roms/transbot.sms')
memory.loadCart(cartridge)

while True:
    print(cpu)

    decoded = decode(cpu.pc.reg, memory)
    print(f'\n {decoded.mnemonic}')
    print('-' * 95)

    try:
        cycles = instructions[decoded.instruction](decoded, cpu, memory, ports)
    except KeyError:
        print(f'Unhandled instruction 0x{decoded.instruction:06X}, {decoded.mnemonic}')
        exit()
