
import getopt
import sms
import sys

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


def _ddcb_prefix (pc) :

    opcode = sms.readByte (pc)

    c = 1
    mnemonic = None
    immediate = None
    displacement = None

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 0 :
        if z != 6 :
            displacement = sms.readByte (pc + c)
            c+= 1
            mnemonic = 'LD {0}, {1} (IX+{2})'.format (table_r[z], table_rot[y], displacement)
        else :
            displacement = sms.readByte (pc + c)
            c+= 1
            mnemonic = '{0} (IX+{1})'.format (table_rot[y], displacement)

    elif x == 1 :
        mnemonic = 'BIT {0}, {1}'.format (y, table_r[z])

    elif x == 2 :
        if z != 6 :
            displacement = sms.readByte (pc + c)
            c+= 1
            mnemonic = 'LD {0}, RES {1}, (IX+{2})'.format (table_r[z], y, displacement)
        else :
            displacement = sms.readByte (pc + c)
            c+= 1
            mnemonic = 'RES {0}, (IX+{1})'.format (y, displacement)

    elif x == 3 :
        if z != 6 :
            displacement = sms.readByte (pc + c)
            c+= 1
            mnemonic = 'LD {0}, SET {1}, (IX+{2})'.format (table_r[z], y, displacement)
        else :
            displacement = sms.readByte (pc + c)
            c+= 1
            mnemonic = 'SET {0}, (IX+{1})'.format (y, displacement)

    return c, 0xDDCB, opcode, mnemonic, displacement, immediate


def _fdcb_prefix (pc) :

    opcode = sms.readByte (pc)

    c = 1
    mnemonic = None
    immediate = None
    displacement = None

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 0 :
        if z != 6 :
            displacement = sms.readByte (pc + c)
            c+= 1
            mnemonic = 'LD {0}, {1} (IY+{2})'.format (table_r[z], table_rot[y], displacement)
        else :
            displacement = sms.readByte (pc + c)
            c+= 1
            mnemonic = '{0} (IY+{1})'.format (table_rot[y], displacement)

    elif x == 1 :
        mnemonic = 'BIT {0}, {1}'.format (y, table_r[z])

    elif x == 2 :
        if z != 6 :
            displacement = sms.readByte (pc + c)
            c+= 1
            mnemonic = 'LD {0}, RES {1}, (IY+{2})'.format (table_r[z], y, displacement)
        else :
            displacement = sms.readByte (pc + c)
            c+= 1
            mnemonic = 'RES {0}, (IY+{1})'.format (y, displacement)

    elif x == 3 :
        if z != 6 :
            displacement = sms.readByte (pc + c)
            c+= 1
            mnemonic = 'LD {0}, SET {1}, (IY+{2})'.format (table_r[z], y, displacement)
        else :
            displacement = sms.readByte (pc + c)
            c+= 1
            mnemonic = 'SET {0}, (IY+{1})'.format (y, displacement)

    return c, 0xFDCB, opcode, mnemonic, displacement, immediate


def _cb_prefix (pc) :

    opcode = sms.readByte(pc)

    c = 1
    mnemonic = None
    displacement = None
    immediate = None

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 0 :
        mnemonic = '{0} {1}'.format (table_rot[y], table_r[z])
    elif x == 1 :
        mnemonic = 'BIT {0}, {1}'.format (y, table_r[z])
    elif x == 2 :
        mnemonic = 'RES {0}, {1}'.format (y, table_r[z])
    elif x == 3 :
        mnemonic = 'SET {0}, {1}'.format (y, table_r[z])

    return c, 0xCB, opcode, mnemonic, displacement, immediate


def _dd_prefix (pc) :

    c = 1
    prefix = None
    mnemonic = None
    displacement = None
    immediate = None

    next_byte = sms.readByte (pc + c)

    if next_byte in (0xDD, 0xED, 0xFD) :
        mnemonic = 'NOP'
        prefix = 0xDD
        opcode = next_byte
    elif next_byte == 0xCB :
        d, prefix, opcode, mnemonic, displacement, immediate = _ddcb_prefix (pc+c)
        c += d
    else :
        d, prefix, opcode, mnemonic, displacement, immediate = decode (pc + c)
        prefix = 0xDD
        c += d

    return c, prefix, opcode, mnemonic, displacement, immediate


def _ed_prefix (pc) :

    opcode = sms.readByte (pc)

    c = 1
    mnemonic = None
    displacement = None
    immediate = None

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 1 :
        if z == 0 :
            if y != 6 :
                mnemonic = 'IN {0}, (C)'.format (table_r[y])
            else :
                mnemonic = 'IN (C)'
        elif z == 1 :
            if y != 6 :
                mnemonic = 'OUT {0}, (C)'.format (table_r[y])
            else :
                mnemonic = 'OUT (C), 0'
        elif z == 2 :
            if q == 0 :
                mnemonic = 'SBC HL, {0}'.format (table_rp[p])
            elif q == 1 :
                mnemonic = 'ADC HL, {0}'.format (table_rp[p])
        elif z == 3 :
            if q == 0 :
                immediate = sms.readWord (pc + c)
                c += 2
                mnemonic = 'LD (0x{0:02X}), {1}'.format (immediate, table_rp[p])
            elif q == 1 :
                immediate = sms.readWord (pc + c)
                c += 2
                mnemonic = 'LD {0}, (0x{1:02X})'.format (table_rp[p], immediate)
        elif z == 4 :
            mnemonic = 'NEG'
        elif z == 5 :
            if y != 1 :
                mnemonic = 'RETN'
            else :
                mnemonic = 'RETI'
        elif z == 6 :
            mnemonic = 'IM {0}'.format (table_im[y])
        elif z == 7 :
            mnemonic = ['LD I, A', 'LD R, A', 'LD A, I', 'LD A, R', 'RRD', 'RLD', 'NOP', 'NOP'][y]

    elif x == 2 :
        if z <= 3 :
            if y >= 4 :
                mnemonic = table_bli[y-4][z]

    return c, 0xED, opcode, mnemonic, displacement, immediate


def _fd_prefix (pc) :

    c = 1
    prefix = None
    displacement = None
    immediate = None
    mnemonic = None

    next_byte = sms.readByte (pc + c)

    if next_byte in (0xDD, 0xED, 0xFD) :
        mnemonic = 'NOP'
        prefix = 0xFD
        opcode = next_byte
    elif next_byte == 0xCB :
        d, prefix, opcode, mnemonic, displacement, immediate = _fdcb_prefix (pc + c)
        c += d
    else :
        d, prefix, opcode, mnemonic, displacement, immediate = decode (pc + c)
        prefix = 0xFD
        c += d

    return c, prefix, opcode, mnemonic, displacement, immediate


# Decodes the mnemonic at 'pc'.
# Implement the alogrithm found here: http://www.z80.info/decoding.htm
# Returns the number of bytes read.
def decode (pc) :

    # Get the opcode.
    opcode = sms.readByte (pc)

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    c = 1
    prefix = 0
    displacement = None
    immediate = None
    mnemonic = None

    if x == 0 :
        if z == 0 :
            if y == 0 :
                mnemonic = 'NOP'
            elif y == 1 :
                mnemonic = "EX AF, AF'"
            elif y == 2 :
                displacement = sms.readByte(pc+c)
                c += 1
                mnemonic = 'DJNZ {0}'.format (displacement)
            elif y == 3 :
                displacement = sms.readByte(pc+c)
                c += 1
                mnemonic = 'JR {0}'.format (displacement)
            elif y in (4, 5, 6, 7) :
                displacement = sms.readByte(pc+c)
                c += 1
                mnemonic = 'JR {0}, {1}'.format (table_cc[y-4], displacement)

        elif z == 1 :
            if q == 0 :
                immediate = sms.readWord(pc + c)
                c += 2
                mnemonic = 'LD {0}, 0x{1:04X}'.format (table_rp[p], immediate)
            elif q == 1 :
                mnemonic = 'ADD HL, {0}'.format (table_rp[p])

        elif z == 2 :
            if q == 0 :
                if p == 0 :
                    mnemonic = 'LD (BC), A'
                elif p == 1 :
                    mnemonic = 'LD (DE), A'
                elif p == 2 :
                    immediate = sms.readWord(pc + c)
                    c += 2
                    mnemonic = 'LD (0x{0:04X}), HL'.format (immediate)
                elif p == 3 :
                    immediate = sms.readWord(pc + c)
                    c += 2
                    mnemonic = 'LD (0x{0:04X}), A'.format (immediate)

            elif q == 1 :
                if p == 0 :
                    mnemonic = 'LD A, (BC)'
                elif p == 1 :
                    mnemonic = 'LD A, (DE)'
                elif p == 2 :
                    immediate = sms.readWord(pc + c)
                    c += 2
                    mnemonic = 'LD HL, (0x{0:04X})'.format (immediate)
                elif p == 3 :
                    immediate = sms.readWord(pc + c)
                    c += 2
                    mnemonic = 'LD A, (0x{0:04X})'.format (immediate)

        elif z == 3 :
            if q == 0 :
                mnemonic = 'INC {0}'.format (table_rp[p])
            elif q == 1 :
                mnemonic = 'DEC {0}'.format (table_rp[p])

        elif z == 4 :
            mnemonic = 'INC {0}'.format (table_r[y])

        elif z == 5 :
            mnemonic = 'DEC {0}'.format (table_r[y])

        elif z == 6 :
            immediate = sms.readByte(pc)
            c += 1
            mnemonic = 'LD {0}, 0x{1:02X}'.format (table_r[y], immediate)

        elif z == 7 :
            mnemonic = ['RLCA', 'RRCA', 'RLA', 'RRA', 'DAA', 'CPL', 'SCF', 'CCF'][y]

    elif x == 1 :
        if z == 7 and y == 6 :
            mnemonic = 'HALT'
        else :
            mnemonic = 'LD {0}, {1}'.format (table_r[y], table_r[z])

    elif x == 2 :
        mnemonic = '{0} {1}'.format (table_alu[y], table_r[z])

    elif x == 3 :
        if z == 0 :
            mnemonic = 'RET {0}'.format (table_cc[y])
        elif z == 1 :
            if q == 0 :
                mnemonic = 'POP {0}'.format (table_rp2[p])
            elif q == 1 :
                mnemonic = ['RET', 'EXX', 'JP HL', 'LD SP, HL'][p]
        elif z == 2 :
            immediate = sms.readWord(pc + c)
            c += 2
            mnemonic = 'JP {0}, 0x{1:04X}'.format (table_cc[y], immediate)
        elif z == 3 :
            if y == 0 :
                immediate = sms.readWord(pc + c)
                c += 2
                mnemonic = 'JP 0x{0:04X}'.format (immediate)
            elif y == 1 :
                d, prefix, opcode, mnemonic, displacement, immediate = _cb_prefix (pc + c)
                c += d
            elif y == 2 :
                immediate = sms.readByte(pc + c)
                c += 1
                mnemonic = 'OUT (0x{0:02X}), A'.format (immediate)
            elif y == 3 :
                immediate = sms.readByte(pc + c)
                c += 1
                mnemonic = 'IN A, (0x{0:02X})'.format (immediate)
            elif y in (4, 5, 6, 7) :
                mnemonic = ['EX (SP), HL', 'EX DE, HL', 'DI', 'EI'][y-4]
        elif z == 4 :
            immediate = sms.readWord(pc + c)
            c += 2
            mnemonic = 'CALL {0}, 0x{1:04X}'.format (table_cc[y], immediate)
        elif z == 5 :
            if q == 0 :
                mnemonic = 'PUSH {0}'.format (table_rp2[p])
            elif q == 1 :
                if p == 0 :
                    immediate = sms.readWord(pc + c)
                    c += 2
                    mnemonic = 'CALL 0x{0:04X}'.format (immediate)
                elif p == 1 :
                    d, prefix, opcode, mnemonic, displacement, immediate = _dd_prefix (pc + c)
                    c += d
                elif p == 2 :
                    d, prefix, opcode, mnemonic, displacement, immediate = _ed_prefix (pc + c)
                    c += d
                elif p == 3 :
                    d, prefix, opcode, mnemonic, displacement, immediate = _fd_prefix (pc + c)
                    c += d

        elif z == 6 :
            immediate = sms.readByte(pc+c)
            c += 1
            mnemonic = '{0} 0x{1:02X}'.format (table_alu[y], immediate)
        elif z == 7 :
            mnemonic = 'RST {0}'.format (y * 8)

    return c, prefix, opcode, displacement, immediate, mnemonic
