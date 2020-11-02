
table_r = [
    'B',
    'C',
    'D',
    'E',
    'H',
    'L',
    '(HL)',
    'A'
]

table_rp = [
    'BC',
    'DE',
    'HL',
    'SP'
]

table_rp2 = [
    'BC',
    'DE',
    'HL',
    'AF'
]

table_cc = [
    'NZ',
    'Z',
    'NC',
    'C',
    'PO',
    'PE',
    'P',
    'M'
]

table_alu = [
    'ADD A,',
    'ADC A,',
    'SUB',
    'SBC A',
    'AND',
    'XOR',
    'OR',
    'CP'
]

table_rot = [
    'RLC',
    'RRC',
    'RL',
    'RR',
    'SLA',
    'SRA',
    'SLL',
    'SRL'
]

table_im = [
    '0',
    '0/1',
    '1',
    '2',
    '0',
    '0/1',
    '1',
    '2'
]

table_bli = [
    ['LDI', 'CPI', 'INI', 'OUTI'],
    ['LDD', 'CPD', 'IND', 'OUTD'],
    ['LDIR', 'CPIR', 'INIR', 'OTIR'],
    ['LDDR', 'CPDR', 'INDR', 'OTDR']
]


def _ddcb_prefix(pc, byte, word):

    opcode = byte(pc)

    c = 1
    mnemonic = None
    immediate = None
    displacement = None

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 0:
        if z != 6:
            displacement = byte(pc + c)
            c += 1
            mnemonic = f'LD {table_r[z]}, {table_rot[y]} (IX+{displacement})'
        else:
            displacement = byte(pc + c)
            c += 1
            mnemonic = f'{table_rot[y]} (IX+{displacement})'

    elif x == 1:
        mnemonic = f'BIT {y}, {table_r[z]}'

    elif x == 2:
        if z != 6:
            displacement = byte(pc + c)
            c += 1
            mnemonic = 'LD {0}, RES {1}, (IX+{2})'.format(table_r[z], y, displacement)
        else:
            displacement = byte(pc + c)
            c += 1
            mnemonic = 'RES {0}, (IX+{1})'.format(y, displacement)

    elif x == 3:
        if z != 6:
            displacement = byte(pc + c)
            c += 1
            mnemonic = 'LD {0}, SET {1}, (IX+{2})'.format(table_r[z], y, displacement)
        else:
            displacement = byte(pc + c)
            c += 1
            mnemonic = 'SET {0}, (IX+{1})'.format(y, displacement)

    return {
        'bytes': c,
        'prefix': 0xDDCB,
        'opcode': opcode,
        'displacement': displacement,
        'immediate': immediate,
        'mnemonic': mnemonic
    }


def _fdcb_prefix(pc, byte, word):

    opcode = byte(pc)

    c = 1
    mnemonic = None
    immediate = None
    displacement = None

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 0:
        if z != 6:
            displacement = byte(pc + c)
            c += 1
            mnemonic = 'LD {0}, {1} (IY+{2})'.format(table_r[z], table_rot[y], displacement)
        else:
            displacement = byte(pc + c)
            c += 1
            mnemonic = '{0} (IY+{1})'.format(table_rot[y], displacement)

    elif x == 1:
        mnemonic = 'BIT {0}, {1}'.format(y, table_r[z])

    elif x == 2:
        if z != 6:
            displacement = byte(pc + c)
            c += 1
            mnemonic = 'LD {0}, RES {1}, (IY+{2})'.format(table_r[z], y, displacement)
        else:
            displacement = byte(pc + c)
            c += 1
            mnemonic = 'RES {0}, (IY+{1})'.format(y, displacement)

    elif x == 3:
        if z != 6:
            displacement = byte(pc + c)
            c += 1
            mnemonic = 'LD {0}, SET {1}, (IY+{2})'.format(table_r[z], y, displacement)
        else:
            displacement = byte(pc + c)
            c += 1
            mnemonic = 'SET {0}, (IY+{1})'.format(y, displacement)

    return {
        'bytes': c,
        'prefix': 0xFDCB,
        'opcode': opcode,
        'displacement': displacement,
        'immediate': immediate,
        'mnemonic': mnemonic
    }


def _cb_prefix(pc, byte, word):

    opcode = byte(pc)

    c = 1
    mnemonic = None
    displacement = None
    immediate = None

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 0:
        mnemonic = '{0} {1}'.format(table_rot[y], table_r[z])
    elif x == 1:
        mnemonic = 'BIT {0}, {1}'.format(y, table_r[z])
    elif x == 2:
        mnemonic = 'RES {0}, {1}'.format(y, table_r[z])
    elif x == 3:
        mnemonic = 'SET {0}, {1}'.format(y, table_r[z])

    return {
        'bytes': c,
        'prefix': 0xCB,
        'opcode': opcode,
        'displacement': displacement,
        'immediate': immediate,
        'mnemonic': mnemonic
    }


def _dd_prefix(pc, byte, word):

    c = 1
    next_byte = byte(pc + c)

    if next_byte in (0xDD, 0xED, 0xFD):

        decoded = {
            'bytes': 0,
            'prefix': 0xDD,
            'opcode': next_byte,
            'displacement': None,
            'immediate': None,
            'mnemonic': 'NOP'
        }

    elif next_byte == 0xCB:
        decoded = _ddcb_prefix(pc+c)
    else:
        decoded(pc + c)
        decoded['prefix'] = 0xDD

    decoded['bytes'] += c
    return decoded


def _ed_prefix(pc, byte, word):

    opcode = byte(pc)

    c = 1
    mnemonic = None
    displacement = None
    immediate = None

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 1:
        if z == 0:
            if y != 6:
                mnemonic = 'IN {0}, (C)'.format(table_r[y])
            else:
                mnemonic = 'IN (C)'
        elif z == 1:
            if y != 6:
                mnemonic = 'OUT {0}, (C)'.format(table_r[y])
            else:
                mnemonic = 'OUT (C), 0'
        elif z == 2:
            if q == 0:
                mnemonic = 'SBC HL, {0}'.format(table_rp[p])
            elif q == 1:
                mnemonic = 'ADC HL, {0}'.format(table_rp[p])
        elif z == 3:
            if q == 0:
                immediate = word(pc + c)
                c += 2
                mnemonic = 'LD (0x{0:02X}), {1}'.format(immediate, table_rp[p])
            elif q == 1:
                immediate = word(pc + c)
                c += 2
                mnemonic = 'LD {0}, (0x{1:02X})'.format(table_rp[p], immediate)
        elif z == 4:
            mnemonic = 'NEG'
        elif z == 5:
            if y != 1:
                mnemonic = 'RETN'
            else:
                mnemonic = 'RETI'
        elif z == 6:
            mnemonic = 'IM {0}'.format(table_im[y])
        elif z == 7:
            mnemonic = ['LD I, A', 'LD R, A', 'LD A, I', 'LD A, R', 'RRD', 'RLD', 'NOP', 'NOP'][y]

    elif x == 2:
        if z <= 3:
            if y >= 4:
                mnemonic = table_bli[y-4][z]

    return {
        'bytes': c,
        'prefix': 0xED,
        'opcode': opcode,
        'displacement': displacement,
        'immediate': immediate,
        'mnemonic': mnemonic
    }


def _fd_prefix(pc, byte, word):

    c = 1
    next_byte = byte(pc + c)

    if next_byte in (0xDD, 0xED, 0xFD):

        decoded = {
            'bytes': 0,
            'prefix': 0xFD,
            'opcode': next_byte,
            'displacement': None,
            'immediate': None,
            'mnemonic': 'NOP'
        }

    elif next_byte == 0xCB:
        decoded = _fdcb_prefix(pc + c)

    else:
        decoded = decode(pc + c)
        decoded['prefix'] = 0xFD

    decoded['bytes'] += c
    return decoded


# Decodes the mnemonic at 'pc'.
# Implement the alogrithm found here: http://www.z80.info/decoding.htm
# Returns the number of bytes read.
def decode(pc, byte, word):

    def _signed_byte(pos):
        b = byte(pos)
        if b > 127:
            b = (256 - b) * -1
        return b

    # Get the opcode.
    opcode = byte(pc)

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    c = 1

    decoded = {
        'bytes': c,
        'prefix': 0,
        'opcode': opcode,
        'displacement': None,
        'immediate': None,
        'mnemonic': None
    }

    if x == 0:
        if z == 0:
            if y == 0:
                decoded['mnemonic'] = 'NOP'
            elif y == 1:
                decoded['mnemonic'] = "EX AF, AF'"
            elif y == 2:
                decoded['displacement'] = byte(pc+c)
                decoded['bytes'] += 1
                decoded['mnemonic'] = f'DJNZ {decoded["displacement"]}'
            elif y == 3:
                decoded['displacement'] = _signed_byte(pc+c)
                decoded['bytes'] += 1
                decoded['mnemonic'] = f'JR {decoded["displacement"]}'
            elif y in (4, 5, 6, 7):
                decoded['displacement'] = _signed_byte(pc+c)
                decoded['bytes'] += 1
                decoded['mnemonic'] = f'JR {table_cc[y-4]}, {decoded["displacement"]}'

        elif z == 1:
            if q == 0:
                decoded['immediate'] = word(pc + c)
                decoded['bytes'] += 2
                decoded['mnemonic'] = f'LD {table_rp[p]}, 0x{decoded["immediate"]:04X}'
            elif q == 1:
                decoded['mnemonic'] = f'ADD HL, {table_rp[p]}'

        elif z == 2:
            if q == 0:
                if p == 0:
                    decoded['mnemonic'] = 'LD (BC), A'
                elif p == 1:
                    decoded['mnemonic'] = 'LD (DE), A'
                elif p == 2:
                    decoded['immediate'] = word(pc + c)
                    decoded['bytes'] += 2
                    decoded['mnemonic'] = f'LD (0x{decoded["immediate"]:04X}), HL'
                elif p == 3:
                    decoded['immediate'] = word(pc + c)
                    decoded['bytes'] += 2
                    decoded['mnemonic'] = f'LD (0x{decoded["immediate"]:04X}), A'

            elif q == 1:
                if p == 0:
                    decoded['mnemonic'] = 'LD A, (BC)'
                elif p == 1:
                    decoded['mnemonic'] = 'LD A, (DE)'
                elif p == 2:
                    decoded['immediate'] = word(pc + c)
                    decoded['bytes'] += 2
                    decoded['mnemonic'] = f'LD HL, (0x{decoded["immediate"]:04X})'
                elif p == 3:
                    decoded['immediate'] = word(pc + c)
                    decoded['bytes'] += 2
                    decoded['mnemonic'] = f'LD A, (0x{decoded["immediate"]:04X})'

        elif z == 3:
            if q == 0:
                decoded['mnemonic'] = f'INC {table_rp[p]}'
            elif q == 1:
                decoded['mnemonic'] = f'DEC {table_rp[p]}'

        elif z == 4:
            decoded['mnemonic'] = f'INC {table_r[y]}'

        elif z == 5:
            decoded['mnemonic'] = f'DEC {table_r[y]}'

        elif z == 6:
            decoded['immediate'] = byte(pc + c)
            decoded['bytes'] += 1
            decoded['mnemonic'] = f'LD {table_r[y]}, 0x{decoded["immediate"]:02X}'

        elif z == 7:
            decoded['mnemonic'] = ['RLCA', 'RRCA', 'RLA', 'RRA', 'DAA', 'CPL', 'SCF', 'CCF'][y]

    elif x == 1:
        if z == 7 and y == 6:
            decoded['mnemonic'] = 'HALT'
        else:
            decoded['mnemonic'] = f'LD {table_r[y]}, {table_r[z]}'

    elif x == 2:
        decoded['mnemonic'] = f'{table_alu[y]} {table_r[z]}'

    elif x == 3:
        if z == 0:
            decoded['mnemonic'] = f'RET {table_cc[y]}'
        elif z == 1:
            if q == 0:
                decoded['mnemonic'] = f'POP {table_rp2[p]}'
            elif q == 1:
                decoded['mnemonic'] = ['RET', 'EXX', 'JP HL', 'LD SP, HL'][p]
        elif z == 2:
            decoded['immediate'] = word(pc + c)
            decoded['bytes'] += 2
            decoded['mnemonic'] = f'JP {table_cc[y]}, 0x{decoded["immediate"]:04X}'
        elif z == 3:
            if y == 0:
                decoded['immediate'] = word(pc + c)
                decoded['bytes'] += 2
                decoded['mnemonic'] = f'JP 0x{decoded["immediate"]:04X}'
            elif y == 1:
                decoded = _cb_prefix(pc + c)
            elif y == 2:
                decoded['immediate'] = byte(pc + c)
                decoded['bytes'] += 1
                decoded['mnemonic'] = f'OUT (0x{decoded["immediate"]:02X}), A'
            elif y == 3:
                decoded['immediate'] = byte(pc + c)
                decoded['bytes'] += 1
                decoded['mnemonic'] = f'IN A, (0x{decoded["immediate"]:02X})'
            elif y in (4, 5, 6, 7):
                decoded['mnemonic'] = ['EX (SP), HL', 'EX DE, HL', 'DI', 'EI'][y-4]
        elif z == 4:
            decoded['immediate'] = word(pc + c)
            decoded['bytes'] += 2
            decoded['mnemonic'] = f'CALL {table_cc[y]}, 0x{decoded["immediate"]:04X}'
        elif z == 5:
            if q == 0:
                decoded['mnemonic'] = 'PUSH {table_rp2[p]}'
            elif q == 1:
                if p == 0:
                    decoded['immediate'] = word(pc + c)
                    decoded['bytes'] += 2
                    decoded['mnemonic'] = f'CALL 0x{0:04X}'
                elif p == 1:
                    decoded = _dd_prefix(pc + c, byte, word)
                    decoded['bytes'] += 1
                elif p == 2:
                    decoded = _ed_prefix(pc + c, byte, word)
                    decoded['bytes'] += 1
                elif p == 3:
                    decoded = _fd_prefix(pc + c, byte, word)
                    decoded['bytes'] += 1

        elif z == 6:
            decoded['immediate'] = byte(pc+c)
            decoded['bytes'] += 1
            decoded['mnemonic'] = f'{table_alu[y]} 0x{decoded["immediate"]:02X}'
        elif z == 7:
            decoded['mnemonic'] = f'RST {y * 8}'

    return decoded
