
class BadInstruction(Exception):
    def __init__(self, decoded, cpu):
        self.decoded = decoded
        self.pc = cpu.pc.reg


def nop(decoded, cpu, *args):
    cpu.pc.reg += decoded.bytes
    return 4


def ld_c_n(decoded, cpu, *args):
    cpu.bc.lo = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 7


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


def jr_z_n(decoded, cpu, *args):
    if cpu.z_flag:
        cpu.pc.reg += decoded.immediate
        cycles = 12
    else:
        cpu.pc.reg += decoded.bytes
        cycles = 7

    return cycles


def ld_sp_nn(decoded, cpu, *args):
    cpu.sp.reg = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 10


def ld_nni_a(decoded, cpu, memory, *args):
    memory.write(decoded.immediate, cpu.af.hi)
    cpu.pc.reg += decoded.bytes
    return 13


def ld_hli_n(decoded, cpu, memory, *args):
    memory.write(cpu.hl.reg, decoded.immediate)
    cpu.pc.reg += decoded.bytes
    return 10


def ld_a_n(decoded, cpu, *args):
    cpu.af.hi = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 7


def or_c(decoded, cpu, *args):
    a = cpu.af.hi | cpu.bc.lo
    cpu.af.hi = a

    if a == 0:
        cpu.z_set()
    else:
        cpu.z_reset()

    if (a & 0x80) != 0:
        cpu.s_set()
    else:
        cpu.s_reset()

    cpu.h_reset()
    # TODO parity
    cpu.n_reset()
    cpu.c_reset()

    cpu.pc.reg += decoded.bytes
    return 4


def ret(decoded, cpu, memory, *args):
    cpu.sp.reg += 2
    cpu.pc.reg = memory.read_word(cpu.sp.reg)
    return 10

def jp_nn(decoded, cpu, *args):
    cpu.pc.reg = decoded.immediate
    return 10


def call_nn(decoded, cpu, memory, *args):
    memory.write_word(cpu.sp.reg, cpu.pc.reg + decoded.bytes)
    cpu.sp.reg -= 2
    cpu.pc.reg = decoded.immediate
    return 17


def out_n_a(decoded, cpu, memory, ports):
    ports.write(decoded.immediate, cpu.af.hi)
    cpu.pc.reg += decoded.bytes
    return 11


def in_a_n(decoded, cpu, memory, ports):
    cpu.af.hi = ports.read(decoded.immediate)
    cpu.pc.reg += decoded.bytes
    return 11


def di(decoded, cpu, *args):
    # TODO implement
    cpu.pc.reg += decoded.bytes
    return 4


def cp_n(decoded, cpu, *args):
    a = cpu.af.hi - decoded.immediate

    if a & 0x80:
        cpu.s_set()
    else:
        cpu.s_reset()

    if a == 0:
        cpu.z_set()
    else:
        cpu.z_reset()

    if ((cpu.af.hi & 0xF) + (decoded.immediate & 0xF)) & 0x10 == 0x10:
        cpu.h_set()
    else:
        cpu.h_reset()

    if a > 0x7F:
        cpu.pv_set()
    elif a < -0x80:
        cpu.pv_set()
    else:
        cpu.pv_reset()

    cpu.n_set()

    if a < 0:
        cpu.c_set()
    else:
        cpu.c_reset()

    cpu.pc.reg += decoded.bytes
    return 7


def im_1(decoded, cpu, *args):
    # TODO implement
    cpu.pc.reg += decoded.bytes
    return 8


def ldir(decoded, cpu, memory, *args):
    if cpu.bc.reg:
        memory.write(cpu.de.reg, memory.read(cpu.hl.reg))
        cpu.hl.reg += 1
        cpu.de.reg += 1
        cpu.bc.reg -= 1
        cycles = 21
    else:
        cycles = 16
        cpu.pc.reg += decoded.bytes

    cpu.h_reset()
    cpu.pv_reset()
    cpu.n_reset()
    return cycles


_instructions = {
    0x00: nop,
    0x01: ld_bc_nn,
    0x0E: ld_c_n,
    0x11: ld_de_nn,
    0x21: ld_hl_nn,
    0x28: jr_z_n,
    0x31: ld_sp_nn,
    0x32: ld_nni_a,
    0x36: ld_hli_n,
    0x3E: ld_a_n,
    0xB1: or_c,
    0xC9: ret,
    0xC3: jp_nn,
    0xCD: call_nn,
    0xD3: out_n_a,
    0xDB: in_a_n,
    0xF3: di,
    0xFE: cp_n,
    0xED56: im_1,
    0xEDB0: ldir
}

def execute(decoded, cpu, memory, ports):
    try:
        return _instructions[decoded.instruction](decoded, cpu, memory, ports)
    except KeyError:
        raise BadInstruction(decoded, cpu)
