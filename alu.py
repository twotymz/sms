
def add_16_16(cpu, a, b):
    """ Add 2 16-bit values and return the results.

    Sets the Z80 flags appropriately.

    Args:
        cpu (Z80)
        a (int)
        b (int)

    Returns:
        int
    """
    r = (a + b)

    # TODO set half-carry
    cpu.n_reset()
    if r > 0xFFFF:
        cpu.c_set()
    else:
        cpu.c_reset()

    return r & 0xFFFF


def bitwise_or(cpu, v):
    """ Bitwise OR v and the accumulator.

    Sets the Z80 flags appropriately.

    Args:
        cpu (Z80)
        v (int)

    Returns:
        int: the result of accumulator | v
    """
    r = cpu.af.hi | v

    if (r & 0x80) != 0:
        cpu.s_set()
    else:
        cpu.s_reset()

    if r == 0:
        cpu.z_set()
    else:
        cpu.z_reset()

    cpu.h_reset()
    # TODO parity
    cpu.n_reset()
    cpu.c_reset()
    return r


def bitwise_xor(cpu, v):
    """ Bitwise XOR v and the accumulator.

    Sets the Z80 flags appropriately.

    Args:
        cpu (Z80)
        v (int)

    Returns:
        int: the resuls of accumulator ^ v
    """
    r = (cpu.af.hi ^ v) & 0xFF

    if (r & 0x80) != 0:
        cpu.s_set()
    else:
        cpu.s_reset()

    if r == 0:
        cpu.z_set()
    else:
        cpu.z_reset()

    cpu.h_reset()
    # TODO set pv based on parity
    cpu.n_reset()
    cpu.c_reset()
    return r
