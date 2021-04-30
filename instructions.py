

def nop(decoded, cpu, memory):
    return 4


def ld_bc_nn(decoded, cpu, memory):
    cpu.bc.reg = decoded.immediate
    return 10


def ld_de_nn(decoded, cpu, memory):
    cpu.de.reg = decoded.immediate
    return 10


def ld_hl_nn(decoded, cpu, memory):
    cpu.hl.reg = decoded.immediate
    return 10


def ld_sp_nn(decoded, cpu, memory):
    cpu.sp.reg = decoded.immediate
    return 10


def ld_hli_n(decoded, cpu, memory):
    memory.writeByte(cpu.hl.reg, decoded.immediate)
    return 10 


def jp_nn(decoded, cpu, memory):
    cpu.pc.reg = decoded.immediate
    return 10


def di(decoded, cpu, memory):
    return 4


def im_1(decoded, cpu, memory):
    # TODO
    return 8


instructions = {
    0x00: nop,
    0x01: ld_bc_nn,
    0x11: ld_de_nn,
    0x21: ld_hl_nn,
    0x31: ld_sp_nn,
    0x36: ld_hli_n,
    0xC3: jp_nn,
    0xF3: di,
    0xED56: im_1
}
