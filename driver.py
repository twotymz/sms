from z80 import Z80
from cartridge import Cartridge
from memory import Memory
from io_port import IOPort
from vdp import VDP
from psg import PSG
from port_mapper import PortMapper, BadPort
from decode import decode
from instructions import execute, BadInstruction


cartridge = Cartridge()
memory = Memory()
cpu = Z80()
io = IOPort()
vdp = VDP()
psg = PSG()
ports = PortMapper(io, vdp, psg)


cartridge.load('roms/transbot.sms')
memory.load_cart(cartridge)


while True:
    print(cpu)
    decoded = decode(cpu.pc.reg, memory)
    print(f'\n {decoded.mnemonic}')
    print('-' * 95)

    try:
        cycles = execute(decoded, cpu, memory, ports)
    except BadInstruction as e:
        print(f' bad instruction at 0x{e.pc:04X}: {e.decoded.mnemonic} (0x{e.decoded.instruction:06X})')
        exit()
    except BadPort as e:
        print(f' attempted {e.access} access on undefined port at {e.port:02X}')
        exit()
