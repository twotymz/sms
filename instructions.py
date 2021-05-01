import alu


class BadInstruction(Exception):
    def __init__(self, decoded, cpu):
        self.decoded = decoded
        self.pc = cpu.pc.reg


def _exchange_registers(r1, r2):
    t = r1.reg
    r1.reg = r2.reg
    r2.reg = t


def nop(decoded, cpu, *args):
    # 0x00
    cpu.pc.reg += decoded.bytes
    return 4


def ld_bc_nn(decoded, cpu, *args):
    # 0x01
    cpu.bc.reg = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 10


def ld_bci_a(decoded, cpu, memory, *args):
    # 0x02
    memory.write(cpu.bc.reg, cpu.af.hi)
    cpu.pc.reg += decoded.bytes
    return 7


def inc_bc(decoded, cpu, *args):
    # 0x03
    cpu.bc.reg += 1
    cpu.pc.reg += decoded.byts
    return 6


def inc_b(decoded, cpu, *args):
    # 0x04
    cpu.bc.hi += 1
    # TODO set flags
    cpu.pc.reg += decoded.bytes
    return 4


def dec_b(decoded, cpu, *args):
    # 0x05
    cpu.bc.hi -= 1
    # TODO set flags
    cpu.pc.reg += decoded.bytes
    return 4


def ld_b_n(decoded, cpu, *args):
    # 0x06
    cpu.bc.hi = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 7


def rlca(decoded, cpu, *args):
    # 0x07
    bit_7 = (cpu.af.hi & 0x80) >> 7
    cpu.af.hi = (cpu.af.hi << 1) & 0xFF | bit_7

    cpu.h_reset()
    cpu.n_reset()

    if bit_7:
        cpu.c_set()
    else:
        cpu.c_reset()

    cpu.pc.reg += decoded.byes
    return 4


def ex_af_af_(decoded, cpu, *args):
    # 0x08
    _exchange_registers(cpu.af, cpu.af_)
    cpu.pc.reg += decoded.bytes
    return 4


def add_hl_bc(decoded, cpu, *args):
    # 0x09
    cpu.hl.reg = alu.add_16_16(cpu, cpu.hl.reg, cpu.bc.reg)
    cpu.pc.reg += decoded.bytes
    return 11


def ld_a_bci(decoded, cpu, memory, *args):
    # 0x0A
    cpu.af.hi = memory.read(cpu.bc.reg)
    cpu.pc.reg += decoded.bytes
    return 7


def dec_bc(decoded, cpu, *args):
    # 0x0B
    cpu.bc.reg -= 1
    cpu.pc.reg += decoded.bytes
    return 6


def inc_c(decoded, cpu, *args):
    # 0x0C
    cpu.bc.lo += 1
    # TODO set flags
    cpu.pc.reg += decoded.bytes
    return 4


def dec_c(decoded, cpu, *args):
    # 0x0D
    cpu.bc.lo -= 1
    # TODO set flags
    cpu.pc.reg += decoded.bytes
    return 4


def ld_c_n(decoded, cpu, *args):
    # 0x0E
    cpu.bc.lo = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 7


def rrca(decoded, cpu, *args):
    # 0x0F
    bit_0 = cpu.af.hi & 0x01
    cpu.af.hi = (cpu.af.hi >> 1) | (bit_0 << 7)

    cpu.h_reset()
    cpu.n_reset()

    if bit_7:
        cpu.c_set()
    else:
        cpu.c_reset()

    cpu.pc.reg += decoded.bytes
    return 4


def djnz(decoded, cpu, *args):
    # 0x10
    cpu.bc.hi = cpu.bc.hi - 1
    cpu.pc.reg += decoded.bytes

    if cpu.bc.hi:
        cpu.pc.reg += decoded.immediate
        cycles = 13
    else:
        cycles = 8

    return cycles


def ld_de_nn(decoded, cpu, *args):
    # 0x11
    cpu.de.reg = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 10


def ld_dei_a(decoded, cpu, memory, *args):
    # 0x12
    memory.write(cpu.de.reg, cpu.af.hi)
    cpu.pc.reg += decoded.bytes
    return 7


def inc_de(decoded, cpu, *args):
    # 0x13
    cpu.de.reg += 1
    cpu.pc.reg += decoded.bytes
    return 6

def inc_d(decoded, cpu, *args):
    # 0x14
    cpu.de.hi += 1
    # TODO set flags
    cpu.pc.reg += decoded.bytes
    return 4


def dec_d(decoded, cpu, *args):
    # 0x15
    cpu.de.hi -= 1
    # TODO set flags
    cpu.pc.reg += decoded.bytes
    return 4


def ld_d_n(decoded, cpu, *args):
    # 0x16
    cpu.de.hi = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 7


def rla(decoded, cpu, *args):
    # 0x17
    bit_7 = cpu.af.hi & 0x80
    cpu.af.hi = cpu.af.hi << 1 | cpu.c_flag

    cpu.h_reset()
    cpu.n_reset()

    if bit_7:
        cpu.c_set()
    else:
        cpu.c_reset()

    cpu.pc.reg += decoded.bytes
    return 4


def jr_n(decoded, cpu, *args):
    # 0x18
    cpu.pc.reg += decoded.bytes + decoded.immediate
    return 12


def add_hl_de(decoded, cpu, *args):
    # 0x19
    cpu.hl.reg = alu.add_16_16(cpu, cpu.hl.reg, cpu.de.reg)
    cpu.pc.reg += decoded.bytes
    return 11


def ld_a_dei(decoded, cpu, memory, *args):
    # 0x1A
    cpu.af.hi = memory.read(cpu.de.reg)
    cpu.pc.reg += decoded.bytes
    return 7


def dec_de(decoded, cpu, *args):
    # 0x1B
    cpu.de.reg -= 1
    cpu.pc.reg += decoded.bytes
    return 6


def inc_e(decoded, cpu, *args):
    # 0x1C
    cpu.de.lo += 1
    # TODO set flags
    cpu.pc.reg += decoded.bytes
    return 4


def ld_e_n(decoded, cpu, *args):
    # 0x1D
    cpu.de.lo = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 7


def rra(decoded, cpu, *args):
    # 0x1F
    bit_0 = cpu.af.hi & 0x01
    cpu.af.hi = (cpu.af.hi >> 1) | (cpu.af.c_flag << 7)

    cpu.h_reset()
    cpu.n_reset()
    if bit_0:
        cpu.c_set()
    else:
        cpu.c_reset()

    cpu.pc.reg += decoded.bytes
    return 4


def ld_hl_nn(decoded, cpu, *args):
    # 0x21
    cpu.hl.reg = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 10


def ld_nni_hl(decoded, cpu, memory, *args):
    # 0x22
    memory.write_word(decoded.immediate, cpu.hl.reg)
    cpu.pc.reg += decoded.bytes
    return 16


def jr_z_n(decoded, cpu, *args):
    # 0x28
    cpu.pc.reg += decoded.bytes
    if cpu.z_flag:
        cpu.pc.reg += decoded.immediate
        cycles = 12
    else:
        cycles = 7

    return cycles


def ld_sp_nn(decoded, cpu, *args):
    # 0x31
    cpu.sp.reg = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 10


def ld_nni_a(decoded, cpu, memory, *args):
    # 0x32
    memory.write(decoded.immediate, cpu.af.hi)
    cpu.pc.reg += decoded.bytes
    return 13


def ld_hli_n(decoded, cpu, memory, *args):
    # 0x36
    memory.write(cpu.hl.reg, decoded.immediate)
    cpu.pc.reg += decoded.bytes
    return 10


def jr_c_n(decoded, cpu, *args):
    # 0x38
    cpu.pc.reg += decoded.bytes
    if cpu.c_flag:
        cpu.pc.reg += decoded.immediate
        cycles = 12
    else:
        cycles = 7

    return cycles


def ld_a_n(decoded, cpu, *args):
    # 0x3E
    cpu.af.hi = decoded.immediate
    cpu.pc.reg += decoded.bytes
    return 7


def xor_a(decoded, cpu, *args):
    # 0xAF
    cpu.af.hi = alu.bitwise_xor(cpu, cpu.af.hi)
    cpu.pc.reg += decoded.bytes
    return 4


def or_c(decoded, cpu, *args):
    # 0xB1
    cpu.af.hi = alu.bitwise_or(cpu, cpu.bc.lo)
    cpu.pc.reg += decoded.bytes
    return 4


def ret(decoded, cpu, memory, *args):
    # 0xC9
    cpu.sp.reg += 2
    cpu.pc.reg = memory.read_word(cpu.sp.reg)
    return 10


def jp_nn(decoded, cpu, *args):
    # 0xC3
    cpu.pc.reg = decoded.immediate
    return 10


def call_nn(decoded, cpu, memory, *args):
    # 0xCD
    memory.write_word(cpu.sp.reg, cpu.pc.reg + decoded.bytes)
    cpu.sp.reg -= 2
    cpu.pc.reg = decoded.immediate
    return 17


def out_n_a(decoded, cpu, memory, ports):
    # 0xD3
    ports.write(decoded.immediate, cpu.af.hi)
    cpu.pc.reg += decoded.bytes
    return 11


def in_a_n(decoded, cpu, memory, ports):
    # 0xDB
    cpu.af.hi = ports.read(decoded.immediate)
    cpu.pc.reg += decoded.bytes
    return 11


def exx(decoded, cpu, *args):
    # 0xD9
    _exchange_registers(cpu.bc, cpu.bc_)
    _exchange_registers(cpu.hl, cpu.hl_)
    _exchange_registers(cpu.de, cpu.de_)
    cpu.pc.reg += decoded.bytes
    return 4


def di(decoded, cpu, *args):
    # 0xF3
    # TODO implement
    cpu.pc.reg += decoded.bytes
    return 4


def cp_n(decoded, cpu, *args):
    # 0xFE
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
    # 0xED56
    # TODO implement
    cpu.pc.reg += decoded.bytes
    return 8


def ldir(decoded, cpu, memory, *args):
    # 0xEDB0
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


def otir(decoded, cpu, memory, port):
    # 0xEDB3
    if cpu.bc.hi:
        port.write(cpu.bc.lo, memory.read(cpu.hl.reg))
        cpu.hl.reg += 1
        cpu.bc.hi -= 1
        cycles = 21
    else:
        cycles = 16
        cpu.pc.reg += decoded.bytes

    cpu.z_set()
    cpu.n_set()
    return cycles


_instructions = {
    0x00: nop,
    0x01: ld_bc_nn,
    0x06: ld_b_n,
    0x0E: ld_c_n,
    0x10: djnz,
    0x11: ld_de_nn,
    0x19: add_hl_de,
    0x21: ld_hl_nn,
    0x22: ld_nni_hl,
    0x28: jr_z_n,
    0x31: ld_sp_nn,
    0x32: ld_nni_a,
    0x36: ld_hli_n,
    0x38: jr_c_n,
    0x3E: ld_a_n,
    0xAF: xor_a,
    0xB1: or_c,
    0xC9: ret,
    0xC3: jp_nn,
    0xCD: call_nn,
    0xD3: out_n_a,
    0xDB: in_a_n,
    0xD9: exx,
    0xF3: di,
    0xFE: cp_n,
    0xED56: im_1,
    0xEDB0: ldir,
    0xEDB3: otir
}

def execute(decoded, cpu, memory, ports):
    try:
        return _instructions[decoded.instruction](decoded, cpu, memory, ports)
    except KeyError:
        raise BadInstruction(decoded, cpu)
