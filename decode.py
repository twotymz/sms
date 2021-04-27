from dataclasses import dataclass

@dataclass
class Decoded:
    bytes: int = 0
    prefix: int = 0
    opcode: int = 0
    displacement: int = 0
    immediate: int = 0
    mnemonic: str = None


_table_r = [
    'B',
    'C',
    'D',
    'E',
    'H',
    'L',
    '(HL)',
    'A'
]

_table_rp = [
    'BC',
    'DE',
    'HL',
    'SP'
]

_table_rp2 = [
    'BC',
    'DE',
    'HL',
    'AF'
]

_table_cc = [
    'NZ',
    'Z',
    'NC',
    'C',
    'PO',
    'PE',
    'P',
    'M'
]

_table_alu = [
    'ADD A,',
    'ADC A,',
    'SUB',
    'SBC A',
    'AND',
    'XOR',
    'OR',
    'CP'
]

_table_rot = [
    'RLC',
    'RRC',
    'RL',
    'RR',
    'SLA',
    'SRA',
    'SLL',
    'SRL'
]

_table_im = [
    '0',
    '0/1',
    '1',
    '2',
    '0',
    '0/1',
    '1',
    '2'
]

_table_bli = [
    ['LDI', 'CPI', 'INI', 'OUTI'],
    ['LDD', 'CPD', 'IND', 'OUTD'],
    ['LDIR', 'CPIR', 'INIR', 'OTIR'],
    ['LDDR', 'CPDR', 'INDR', 'OTDR']
]


def _ddcb_prefix(pc, byte, word):

    opcode = byte(pc)
    decoded = Decoded(1, 0xDDCB, opcode)

    #c = 1
    #mnemonic = None
    #immediate = 0
    #displacement = 0

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 0:
        if z != 6:
            decoded.displacement = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'LD {_table_r[z]}, {_table_rot[y]} (IX+{decoded.displacement})'
        else:
            decoded.displacement = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'{_table_rot[y]} (IX+{decoded.displacement})'

    elif x == 1:
        decoded.mnemonic = f'BIT {y}, {_table_r[z]}'

    elif x == 2:
        if z != 6:
            decoded.displacement = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'LD {_table_r[z]}, RES {y}, (IX+{decoded.displacement})'
        else:
            decoded.displacement = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'RES {y}, (IX+{decoded.displacement})'

    elif x == 3:
        if z != 6:
            decoded.displacement = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'LD {_table_r[z]}, SET {y}, (IX+{decoded.displacement})'
        else:
            decoded.displacement = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'SET {y}, (IX+{decoded.displacement})'

    #return Decoded(c, 0xDDCB, opcode, displacement, immediate, mnemonic)
    return decoded


def _fdcb_prefix(pc, byte, word):

    opcode = byte(pc)
    decoded = Decoded(1, 0xFDCB, opcode)

    #mnemonic = None
    #immediate = 0
    #displacement = 0

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 0:
        if z != 6:
            decoded.displacement = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'LD {_table_r[z]}, {_table_rot[y]} (IY+{decoded.displacement})'
        else:
            decoded.displacement = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'{_table_rot[y]} (IY+{decoded.displacement})'

    elif x == 1:
        decoded.mnemonic = f'BIT {y}, {_table_r[z]}'

    elif x == 2:
        if z != 6:
            decoded.displacement = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'LD {_table_r[z]}, RES {y}, (IY+{decoded.displacement})'
        else:
            decoded.displacement = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'RES {y}, (IY+{decoded.displacement})'

    elif x == 3:
        if z != 6:
            decoded.displacement = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'LD {_table_r[z]}, SET {y}, (IY+{decoded.displacement})'
        else:
            decoded.displacement = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'SET {y}, (IY+{decoded.displacement})'

    #return Decoded(c, 0xFDCB, opcode, displacement, immediate, mnemonic)
    return decoded


def _cb_prefix(pc, byte, word):

    opcode = byte(pc)
    decoded = Decoded(1, 0xCB, opcode)

    #c = 1
    #mnemonic = None
    #displacement = 0
    #immediate = 0

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 0:
        decoded.mnemonic = f'{_table_rot[y]} {_table_r[z]}'
    elif x == 1:
        decoded.mnemonic = f'BIT {y}, {_table_r[z]}'
    elif x == 2:
        decoded.mnemonic = f'RES {y}, {_table_r[z]}'
    elif x == 3:
        decoded.mnemonic = f'SET {y}, {_table_r[z]}'

    #return Decoded(c, 0xCB, opcode, displacement, immediate, mnemonic)
    return decoded


def _dd_prefix(pc, byte, word):

    c = 1
    next_byte = byte(pc + c)

    if next_byte in (0xDD, 0xED, 0xFD):
        decoded = Decoded(0, 0xDD, next_byte, None, None, 'NOP')
    elif next_byte == 0xCB:
        decoded = _ddcb_prefix(pc + c, byte, word)
    else:
        decoded = decode(pc + c, byte, word)
        decoded.prefix = 0xDD

    decoded.bytes += c
    return decoded


def _ed_prefix(pc, byte, word):

    opcode = byte(pc)
    decoded = Decoded(1, 0xED, opcode)

    #c = 1
    #mnemonic = None
    #displacement = 0
    #immediate = 0

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 1:
        if z == 0:
            if y != 6:
                decoded.mnemonic = f'IN {_table_r[y]}, (C)'
            else:
                decoded.mnemonic = 'IN (C)'
        elif z == 1:
            if y != 6:
                decoded.mnemonic = f'OUT {_table_r[y]}, (C)'
            else:
                decoded.mnemonic = 'OUT (C), 0'
        elif z == 2:
            if q == 0:
                decoded.mnemonic = f'SBC HL, {_table_rp[p]}'
            elif q == 1:
                decoded.mnemonic = f'ADC HL, {_table_rp[p]}'
        elif z == 3:
            if q == 0:
                decoded.immediate = word(pc + 1)
                decoded.bytes += 2
                decoded.mnemonic = f'LD (0x{decoded.immediate:02X}), {_table_rp[p]}'
            elif q == 1:
                decoded.immediate = word(pc + 1)
                decoded.bytes += 2
                decoded.mnemonic = f'LD {_table_rp[p]}, (0x{decoded.immediate:02X})'
        elif z == 4:
            decoded.mnemonic = 'NEG'
        elif z == 5:
            if y != 1:
                decoded.mnemonic = 'RETN'
            else:
                decoded.mnemonic = 'RETI'
        elif z == 6:
            decoded.mnemonic = f'IM {_table_im[y]}'
        elif z == 7:
            decoded.mnemonic = ['LD I, A', 'LD R, A', 'LD A, I', 'LD A, R', 'RRD', 'RLD', 'NOP', 'NOP'][y]

    elif x == 2:
        if z <= 3:
            if y >= 4:
                decoded.mnemonic = _table_bli[y-4][z]

    #return Decoded(c, 0xED, opcode, displacement, immediate, mnemonic)
    return decoded


def _fd_prefix(pc, byte, word):

    c = 1
    next_byte = byte(pc + c)

    if next_byte in (0xDD, 0xED, 0xFD):
        decoded = Decoded(0, 0xFD, next_byte, None, None, 'NOP')

    elif next_byte == 0xCB:
        decoded = _fdcb_prefix(pc + c, byte, word)

    else:
        decoded = decode(pc + c, byte, word)
        decoded.prefix = 0xFD

    decoded.bytes += c
    return decoded


def decode(pc, byte, word):
    """ Decodes the mnemonic at "pc".

    Implement the alogrithm found here: http://www.z80.info/decoding.htm

    Args:
        pc (int)
        byte (callable) -- a function that returns an 8 bit value at a memory location
        word (callablle) -- a function that returns a 16 bit value at a memory location

    Returns:
        Decoded: the decoded instruction
    """

    def _signed_byte(pos):
        b = byte(pos)
        if b > 127:
            b = (256 - b) * -1
        return b

    # Get the opcode.
    opcode = byte(pc)
    decoded = Decoded(1, 0, opcode)

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    #c = 1

    if x == 0:
        if z == 0:
            if y == 0:
                decoded.mnemonic = 'NOP'
            elif y == 1:
                decoded.mnemonic = "EX AF, AF'"
            elif y == 2:
                decoded.displacement = byte(pc + 1)
                decoded.bytes += 1
                decoded.mnemonic = f'DJNZ {decoded.displacement}'
            elif y == 3:
                decoded.displacement = _signed_byte(pc + 1)
                decoded.bytes += 1
                decoded.mnemonic = f'JR {decoded.displacement}'
            elif y in (4, 5, 6, 7):
                decoded.displacement = _signed_byte(pc + 1)
                decoded.bytes += 1
                decoded.mnemonic = f'JR {_table_cc[y-4]}, {decoded.displacement}'

        elif z == 1:
            if q == 0:
                decoded.immediate = word(pc + 1)
                decoded.bytes += 2
                decoded.mnemonic = f'LD {_table_rp[p]}, 0x{decoded.immediate:04X}'
            elif q == 1:
                decoded.mnemonic = f'ADD HL, {_table_rp[p]}'

        elif z == 2:
            if q == 0:
                if p == 0:
                    decoded.mnemonic = 'LD (BC), A'
                elif p == 1:
                    decoded.mnemonic = 'LD (DE), A'
                elif p == 2:
                    decoded.immediate = word(pc + 1)
                    decoded.bytes += 2
                    decoded.mnemonic = f'LD (0x{decoded.immediate:04X}), HL'
                elif p == 3:
                    decoded.immediate = word(pc + 1)
                    decoded.bytes += 2
                    decoded.mnemonic = f'LD (0x{decoded.immediate:04X}), A'

            elif q == 1:
                if p == 0:
                    decoded.mnemonic = 'LD A, (BC)'
                elif p == 1:
                    decoded.mnemonic = 'LD A, (DE)'
                elif p == 2:
                    decoded.immediate = word(pc + 1)
                    decoded.bytes += 2
                    decoded.mnemonic = f'LD HL, (0x{decoded.immediate:04X})'
                elif p == 3:
                    decoded.immediate = word(pc + 1)
                    decoded.bytes += 2
                    decoded.mnemonic = f'LD A, (0x{decoded.immediate:04X})'

        elif z == 3:
            if q == 0:
                decoded.mnemonic = f'INC {_table_rp[p]}'
            elif q == 1:
                decoded.mnemonic = f'DEC {_table_rp[p]}'

        elif z == 4:
            decoded.mnemonic = f'INC {_table_r[y]}'

        elif z == 5:
            decoded.mnemonic = f'DEC {_table_r[y]}'

        elif z == 6:
            decoded.immediate = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'LD {_table_r[y]}, 0x{decoded.immediate:02X}'

        elif z == 7:
            decoded.mnemonic = ['RLCA', 'RRCA', 'RLA', 'RRA', 'DAA', 'CPL', 'SCF', 'CCF'][y]

    elif x == 1:
        if z == 7 and y == 6:
            decoded.mnemonic = 'HALT'
        else:
            decoded.mnemonic = f'LD {_table_r[y]}, {_table_r[z]}'

    elif x == 2:
        decoded.mnemonic = f'{_table_alu[y]} {_table_r[z]}'

    elif x == 3:
        if z == 0:
            decoded.mnemonic = f'RET {_table_cc[y]}'
        elif z == 1:
            if q == 0:
                decoded.mnemonic = f'POP {_table_rp2[p]}'
            elif q == 1:
                decoded.mnemonic = ['RET', 'EXX', 'JP HL', 'LD SP, HL'][p]
        elif z == 2:
            decoded.immediate = word(pc + 1)
            decoded.bytes += 2
            decoded.mnemonic = f'JP {_table_cc[y]}, 0x{decoded.immediate:04X}'
        elif z == 3:
            if y == 0:
                decoded.immediate = word(pc + 1)
                decoded.bytes += 2
                decoded.mnemonic = f'JP 0x{decoded.immediate:04X}'
            elif y == 1:
                decoded = _cb_prefix(pc + 1, byte, word)
            elif y == 2:
                decoded.immediate = byte(pc + 1)
                decoded.bytes += 1
                decoded.mnemonic = f'OUT (0x{decoded.immediate:02X}), A'
            elif y == 3:
                decoded.immediate = byte(pc + 1)
                decoded.bytes += 1
                decoded.mnemonic = f'IN A, (0x{decoded.immediate:02X})'
            elif y in (4, 5, 6, 7):
                decoded.mnemonic = ['EX (SP), HL', 'EX DE, HL', 'DI', 'EI'][y-4]
        elif z == 4:
            decoded.immediate = word(pc + 1)
            decoded.bytes += 2
            decoded.mnemonic = f'CALL {_table_cc[y]}, 0x{decoded.immediate:04X}'
        elif z == 5:
            if q == 0:
                decoded.mnemonic = f'PUSH {_table_rp2[p]}'
            elif q == 1:
                if p == 0:
                    decoded.immediate = word(pc + 1)
                    decoded.bytes += 2
                    decoded.mnemonic = f'CALL 0x{decoded.immediate:04X}'
                elif p == 1:
                    decoded = _dd_prefix(pc + 1, byte, word)
                    decoded.bytes += 1
                elif p == 2:
                    decoded = _ed_prefix(pc + 1, byte, word)
                    decoded.bytes += 1
                elif p == 3:
                    decoded = _fd_prefix(pc + 1, byte, word)
                    decoded.bytes += 1

        elif z == 6:
            decoded.immediate = byte(pc + 1)
            decoded.bytes += 1
            decoded.mnemonic = f'{_table_alu[y]} 0x{decoded.immediate:02X}'
        elif z == 7:
            decoded.mnemonic = f'RST {y * 8}'

    return decoded
