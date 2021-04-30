

def nop(decoded, cpu, *args):
    cpu.pc.reg += decoded.bytes
    return 4


def ld_bc_nn(decoded, cpu, *args):
    cpu.bc.reg = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 10


def ld_de_nn(decoded, cpu, *args):
    cpu.de.reg = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 10


def ld_hl_nn(decoded, cpu, *args):
    cpu.hl.reg = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 10


def ld_sp_nn(decoded, cpu, *args):
    cpu.sp.reg = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 10


def ld_hli_n(decoded, cpu, memory, *args):
    memory.writeByte(cpu.hl.reg, decoded.immediate)
    cpu.pc.reg += decoded.bytes
    return 10


def ld_a_n(decoded, cpu, *args):
    cpu.af.hi = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 7


def jp_nn(decoded, cpu, *args):
    cpu.pc.reg = decoded.immediate
    return 10


def call_nn(decoded, cpu, memory, *args):
    memory.writeWord(cpu.sp.reg, cpu.pc.reg + 3)
    cpu.sp.reg -= 2
    cpu.pc.reg = decoded.immediate
    return 17


def out_n_a(decoded, cpu, memory, ports):
    ports[decoded.immediate].write(cpu.af.hi)
    cpu.pc.reg += decoded.bytes
    return 11


def in_a_n(decoded, cpu, memory, ports):
    cpu.af.hi = ports[decoded.immediate].read()
    cpu.pc.reg += decoded.bytes
    return 11


def di(decoded, cpu, *args):
    # TODO implement
    cpu.pc.reg += decoded.bytes
    return 4


def im_1(decoded, cpu, *args):
    # TODO implement
    cpu.pc.reg += decoded.bytes
    return 8


def ldir(decoded, cpu, memory, *args):
    if cpu.bc.reg:
        memory.writeByte(cpu.de.reg, memory.readByte(cpu.hl.reg))
        cpu.hl.reg += 1
        cpu.de.reg += 1
        cpu.bc.reg -= 1
        cycles = 21
    else:
        cycles = 16
        cpu.pc.reg += decoded.bytes

    cpu.resetH()
    cpu.resetN()
    cpu.resetPV()
    return cycles

instructions = {
    0x00: nop,
    0x01: ld_bc_nn,
    0x11: ld_de_nn,
    0x21: ld_hl_nn,
    0x31: ld_sp_nn,
    0x36: ld_hli_n,
    0x3E: ld_a_n,
    0xC3: jp_nn,
    0xCD: call_nn,
    0xD3: out_n_a,
    0xDB: in_a_n,
    0xF3: di,
    0xED56: im_1,
    0xEDB0: ldir
}
