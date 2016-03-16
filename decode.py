
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

    opcode = sms.mapper.ram[pc]

    c = 1
    instruction = None
    immediate = None
    displacement = None

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 0 :
        if z != 6 :
            displacement = sms.mapper.ram[pc+c]
            c+= 1
            instruction = 'LD {0}, {1} (IX+{2})'.format (table_r[z], table_rot[y], displacement)
        else :
            displacement = sms.mapper.ram[pc+c]
            c+= 1
            instruction = '{0} (IX+{1})'.format (table_rot[y], displacement)

    elif x == 1 :
        instruction = 'BIT {0}, {1}'.format (y, table_r[z])

    elif x == 2 :
        if z != 6 :
            displacement = sms.mapper.ram[pc+c]
            c+= 1
            instruction = 'LD {0}, RES {1}, (IX+{2})'.format (table_r[z], y, displacement)
        else :
            displacement = sms.mapper.ram[pc+c]
            c+= 1
            instruction = 'RES {0}, (IX+{1})'.format (y, displacement)

    elif x == 3 :
        if z != 6 :
            displacement = sms.mapper.ram[pc+c]
            c+= 1
            instruction = 'LD {0}, SET {1}, (IX+{2})'.format (table_r[z], y, displacement)
        else :
            displacement = sms.mapper.ram[pc+c]
            c+= 1
            instruction = 'SET {0}, (IX+{1})'.format (y, displacement)

    return c, instruction, displacement, immediate


def _fdcb_prefix (pc) :

    opcode = sms.mapper.ram[pc]

    c = 1
    instruction = None
    immediate = None
    displacement = None

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 0 :
        if z != 6 :
            displacement = sms.mapper.ram[pc+c]
            c+= 1
            instruction = 'LD {0}, {1} (IY+{2})'.format (table_r[z], table_rot[y], displacement)
        else :
            displacement = sms.mapper.ram[pc+c]
            c+= 1
            instruction = '{0} (IY+{1})'.format (table_rot[y], displacement)

    elif x == 1 :
        instruction = 'BIT {0}, {1}'.format (y, table_r[z])

    elif x == 2 :
        if z != 6 :
            displacement = sms.mapper.ram[pc+c]
            c+= 1
            instruction = 'LD {0}, RES {1}, (IY+{2})'.format (table_r[z], y, displacement)
        else :
            displacement = sms.mapper.ram[pc+c]
            c+= 1
            instruction = 'RES {0}, (IY+{1})'.format (y, displacement)

    elif x == 3 :
        if z != 6 :
            displacement = sms.mapper.ram[pc+c]
            c+= 1
            instruction = 'LD {0}, SET {1}, (IY+{2})'.format (table_r[z], y, displacement)
        else :
            displacement = sms.mapper.ram[pc+c]
            c+= 1
            instruction = 'SET {0}, (IY+{1})'.format (y, displacement)

    return c, instruction, displacement, immediate


def _cb_prefix (pc) :

    opcode = sms.mapper.ram[pc]

    c = 1
    instruction = None
    displacement = None
    immediate = None

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    if x == 0 :
        instruction = '{0} {1}'.format (table_rot[y], table_r[z])
    elif x == 1 :
        instruction = 'BIT {0}, {1}'.format (y, table_r[z])
    elif x == 2 :
        instruction = 'RES {0}, {1}'.format (y, table_r[z])
    elif x == 3 :
        instruction = 'SET {0}, {1}'.format (y, table_r[z])

    return c, instruction, displacement, immediate


def _dd_prefix (pc) :

    c = 1
    instruction = None
    displacement = None
    immediate = None

    if sms.mapper.ram[pc+c] in (0xDD, 0xED, 0xFD) :
        instruction = 'NOP'
    elif sms.mapper.ram[pc+c] == 0xCB :
        d, instruction, displacement, immediate = _ddcb_prefix (pc+c)
        c += d
    else :
        d, instruction, displacement, immediate = decode (pc + c)
        c += d

    return c, instruction, displacement, immediate


def _ed_prefix (pc) :

    opcode = sms.mapper.ram[pc]

    c = 1
    instruction = None
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
                instruction = 'IN {0}, (C)'.format (table_r[y])
            else :
                instruction = 'IN (C)'
        elif z == 1 :
            if y != 6 :
                instruction = 'OUT {0}, (C)'.format (table_r[y])
            else :
                instruction = 'OUT (C), 0'
        elif z == 2 :
            if q == 0 :
                instruction = 'SBC HL, {0}'.format (table_rp[p])
            elif q == 1 :
                instruction = 'ADC HL, {0}'.format (table_rp[p])
        elif z == 3 :
            if q == 0 :
                immediate = sms.mapper.ram[pc + c] | sms.mapper.ram[pc + c + 1] << 8
                c += 2
                instruction = 'LD (0x{0:02X}), {1}'.format (immediate, table_rp[p])
            elif q == 1 :
                immediate = sms.mapper.ram[pc + c] | sms.mapper.ram[pc + c + 1] << 8
                c += 2
                instruction = 'LD {0}, (0x{1:02X})'.format (table_rp[p], immediate)
        elif z == 4 :
            instruction = 'NEG'
        elif z == 5 :
            if y != 1 :
                instruction = 'RETN'
            else :
                instruction = 'RETI'
        elif z == 6 :
            instruction = 'IM {0}'.format (table_im[y])
        elif z == 7 :
            instruction = ['LD I, A', 'LD R, A', 'LD A, I', 'LD A, R', 'RRD', 'RLD', 'NOP', 'NOP'][y]

    elif x == 2 :
        if z <= 3 :
            if y >= 4 :
                instruction = table_bli[y-4][z]

    return c, instruction, displacement, immediate


def _fd_prefix (pc) :

    c = 1
    instruction = None
    displacement = None
    immediate = None

    if sms.mapper.ram[pc+c] in (0xDD, 0xED, 0xFD) :
        instruction = 'NOP'
    elif sms.mapper.ram[pc+c] == 0xCB :
        d, instruction, displacement, immediate = _fdcb_prefix (pc+c)
        c += d
    else :
        d, instruction, displacement, immediate = decode (pc + c)
        c += d

    return c, instruction, displacement, immediate


# Decodes the instruction at 'pc'.
# Implement the alogrithm found here: http://www.z80.info/decoding.htm
# Returns the number of bytes read.
def decode (pc) :

    # Get the opcode.
    opcode = sms.mapper.ram[pc]

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    c = 1
    instruction = None
    displacement = None
    immediate = None

    if x == 0 :
        if z == 0 :
            if y == 0 :
                instruction = 'NOP'
            elif y == 1 :
                instruction = "EX AF, AF'"
            elif y == 2 :
                displacement = sms.mapper.ram[pc+c]
                c += 1
                instruction = 'DJNZ {0}'.format (displacement)
            elif y == 3 :
                displacement = sms.mapper.ram[pc+c]
                c += 1
                instruction = 'JR {0}'.format (displacement)
            elif y in (4, 5, 6, 7) :
                displacement = sms.mapper.ram[pc+c]
                c += 1
                instruction = 'JR {0}, {1}'.format (table_cc[y-4], displacement)

        elif z == 1 :
            if q == 0 :
                immediate = sms.mapper.ram[pc + c] | sms.mapper.ram[pc + c + 1] << 8
                c += 2
                instruction = 'LD {0}, 0x{1:04X}'.format (table_rp[p], immediate)
            elif q == 1 :
                instruction = 'ADD HL, {0}'.format (table_rp[p])

        elif z == 2 :
            if q == 0 :
                if p == 0 :
                    instruction = 'LD (BC), A'
                elif p == 1 :
                    instruction = 'LD (DE), A'
                elif p == 2 :
                    immediate = sms.mapper.ram[pc + c] | sms.mapper.ram[pc + c + 1] << 8
                    c += 2
                    instruction = 'LD (0x{0:04X}), HL'.format (immediate)
                elif p == 3 :
                    immediate = sms.mapper.ram[pc + c] | sms.mapper.ram[pc + c + 1] << 8
                    c += 2
                    instruction = 'LD (0x{0:04X}), A'.format (immediate)

            elif q == 1 :
                if p == 0 :
                    instruction = 'LD A, (BC)'
                elif p == 1 :
                    instruction = 'LD A, (DE)'
                elif p == 2 :
                    immediate = sms.mapper.ram[pc + c] | sms.mapper.ram[pc + c + 1] << 8
                    c += 2
                    instruction = 'LD HL, (0x{0:04X})'.format (immediate)
                elif p == 3 :
                    immediate = sms.mapper.ram[pc + c] | sms.mapper.ram[pc + c + 1] << 8
                    c += 2
                    instruction = 'LD A, (0x{0:04X})'.format (immediate)

        elif z == 3 :
            if q == 0 :
                instruction = 'INC {0}'.format (table_rp[p])
            elif q == 1 :
                instruction = 'DEC {0}'.format (table_rp[p])

        elif z == 4 :
            instruction = 'INC {0}'.format (table_r[y])

        elif z == 5 :
            instruction = 'DEC {0}'.format (table_r[y])

        elif z == 6 :
            immediate = sms.mapper.ram[pc+c]
            c += 1
            instruction = 'LD {0}, 0x{1:02X}'.format (table_r[y], immediate)

        elif z == 7 :
            instruction = ['RLCA', 'RRCA', 'RLA', 'RRA', 'DAA', 'CPL', 'SCF', 'CCF'][y]

    elif x == 1 :
        if z == 7 and y == 6 :
            instruction = 'HALT'
        else :
            instruction = 'LD {0}, {1}'.format (table_r[y], table_r[z])

    elif x == 2 :
        instruction = '{0} {1}'.format (table_alu[y], table_r[z])

    elif x == 3 :
        if z == 0 :
            instruction = 'RET {0}'.format (table_cc[y])
        elif z == 1 :
            if q == 0 :
                instruction = 'POP {0}'.format (table_rp2[p])
            elif q == 1 :
                instruction = ['RET', 'EXX', 'JP HL', 'LD SP, HL'][p]
        elif z == 2 :
            immediate = sms.mapper.ram[pc + c] | sms.mapper.ram[pc + c + 1] << 8
            c += 2
            instruction = 'JP {0}, 0x{1:04X}'.format (table_cc[y], immediate)
        elif z == 3 :
            if y == 0 :
                immediate = sms.mapper.ram[pc + c] | sms.mapper.ram[pc + c + 1] << 8
                c += 2
                instruction = 'JP 0x{0:04X}'.format (immediate)
            elif y == 1 :
                d, instruction, displacement, immediate = _cb_prefix (pc + c)
                c += d
            elif y == 2 :
                immediate = sms.mapper.ram[pc+c]
                c += 1
                instruction = 'OUT (0x{0:02X}), A'.format (immediate)
            elif y == 3 :
                immediate = sms.mapper.ram[pc+c]
                c += 1
                instruction = 'IN A, (0x{0:02X})'.format (immediate)
            elif y in (4, 5, 6, 7) :
                instruction = ['EX (SP), HL', 'EX DE, HL', 'DI', 'EI'][y-4]
        elif z == 4 :
            immediate = sms.mapper.ram[pc + c] << 8 | sms.mapper.ram[pc + c + 1]
            c += 2
            instruction = 'CALL {0}, 0x{1:04X}'.format (table_cc[y], immediate)
        elif z == 5 :
            if q == 0 :
                instruction = 'PUSH {0}'.format (table_rp2[p])
            elif q == 1 :
                if p == 0 :
                    immediate = sms.mapper.ram[pc + c] | sms.mapper.ram[pc + c + 1] << 8
                    c += 2
                    instruction = 'CALL 0x{0:04X}'.format (immediate)
                elif p == 1 :
                    d, instruction, displacement, immediate = _dd_prefix (pc + c)
                    c += d
                elif p == 2 :
                    d, instruction, displacement, immediate = _ed_prefix (pc + c)
                    c += d
                elif p == 3 :
                    d, instruction, displacement, immediate = _fd_prefix (pc + c)
                    c += d

        elif z == 6 :
            immediate = sms.mapper.ram[pc+c]
            c += 1
            instruction = '{0} 0x{1:02X}'.format (table_alu[y], immediate)
        elif z == 7 :
            instruction = 'RST {0}'.format (y * 8)

    return c, instruction, displacement, immediate
