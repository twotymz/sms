
import sms

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

# Decodes the next instruction.
#
# Args
#   'pc' - where to start reading in 'sms.rom'.
# Returns
#   the number of bytes read.
def decode (pc) :

    # instructions are stored in this format:
    # [prefix] opcode [displacement] [immediate data]

    prefix = None
    c = 0

    # Test for the prefix byte.
    if sms.rom[pc] in (0xCB, 0xDD, 0xED, 0xFD) :
        prefix = sms.rom[pc]
        c += 1

    # Get the opcode.
    opcode = sms.rom[pc+c]
    c += 1

    x = (opcode & 0xC0) >> 6
    y = (opcode & 0x38) >> 3
    z = (opcode & 0x7)
    p = y >> 1
    q = y & 0x1

    instruction = None

    if x == 0 :
        if z == 0 :
            if y == 0 :
                instruction = 'NOP'
            elif y == 1 :
                instruction = "EX AF, AF'"
            elif y == 2 :
                displacement = sms.rom[pc+c]
                c += 1
                instruction = 'DJNZ {0}'.format (displacement)
            elif y == 3 :
                displacement = sms.rom[pc+c]
                c += 1
                instruction = 'JR {0}'.format (displacement)
            elif y in (4, 5, 6, 7) :
                displacement = sms.rom[pc+c]
                c += 1
                instruction = 'JR {0}, {1}'.format (table_cc[y-4], displacement)

        elif z == 1 :
            if q == 0 :
                immediate = sms.rom[pc + c] << 8 | sms.rom[pc + c + 1]
                c += 2
                instruction = 'LD {0}, 0x{1:02X}'.format (table_rp[p], immediate)
            elif q == 1 :
                instruction = 'ADD HL, {0}'.format (table_rp[p])

        elif z == 2 :
            if q == 0 :
                if p == 0 :
                    instruction = 'LD (BC), A'
                elif p == 1 :
                    instruction = 'LD (DE), A'
                elif p == 2 :
                    immediate = sms.rom[pc + c] << 8 | sms.rom[pc + c + 1]
                    c += 2
                    instruction = 'LD (0x{0:02X}), HL'.format (immediate)
                elif p == 3 :
                    immediate = sms.rom[pc + c] << 8 | sms.rom[pc + c + 1]
                    c += 2
                    instruction = 'LD (0x{0:02X}), A'.format (immediate)

            elif q == 1 :
                if p == 0 :
                    instruction = 'LD A, (BC)'
                elif p == 1 :
                    instruction = 'LD A, (DE)'
                elif p == 2 :
                    immediate = sms.rom[pc + c] << 8 | sms.rom[pc + c + 1]
                    c += 2
                    instruction = 'LD HL, (0x{0:02X})'.format (immediate)
                elif p == 3 :
                    immediate = sms.rom[pc + c] << 8 | sms.rom[pc + c + 1]
                    c += 2
                    instruction = 'LD A, (0x{0:02X})'.format (immediate)

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
            immediate = sms.rom[pc+c]
            c += 1
            instruction = 'LD {0}, 0x{1:02X}'.format (table_r[y], immediate)

        elif z == 7 :
            instruction = ['RLCA', 'RRCA', 'RLA', 'RRA', 'DAA', 'CPL', 'SCF', 'CCF'][y]

    elif x == 1 :
        if z == 7 :
            if y == 6 :
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
            immediate = sms.rom[pc + c] << 8 | sms.rom[pc + c + 1]
            c += 2
            instruction = 'JP {0}, 0x{1:02X}'.format (table_cc[y], immediate)
        elif z == 3 :
            if y == 0 :
                immediate = sms.rom[pc + c] << 8 | sms.rom[pc + c + 1]
                c += 2
                instruction = 'JP 0x{0:02X}'.format (immediate)
            elif y == 1 :
                pass
            elif y == 2 :
                immediate = sms.rom[pc+c]
                c += 1
                instruction = 'OUT (0x{0:02X}), A'.format (immediate)
            elif y == 3 :
                immediate = sms.rom[pc+c]
                c += 1
                instruction = 'IN A, (0x{0:02X})'.format (immediate)
            elif y in (4, 5, 6, 7) :
                instruction = ['EX (SP), HL', 'EX DE, HL', 'DI', 'EI'][y-4]
        elif z == 4 :
            immediate = sms.rom[pc + c] << 8 | sms.rom[pc + c + 1]
            c += 2
            instruction = 'CALL {0}, 0x{1:02X}'.format (table_cc[y], immediate)
        elif z == 5 :
            if q == 0 :
                instruction = 'PUSH {0}'.format (table_rp2[p])
            elif q == 1 :
                if p == 0 :
                    immediate = sms.rom[pc + c] << 8 | sms.rom[pc + c + 1]
                    c += 2
                    instruction = 'CALL 0x{0:02X}'.format (immediate)
                elif p == 1 :
                    pass
                elif p == 2 :
                    pass
                elif p == 3 :
                    pass
        elif z == 6 :
            immediate = sms.rom[pc+c]
            c += 1
            instruction = '{0} 0x{1:02X}'.format (table_alu[y], immediate)
        elif z == 7 :
            instruction = 'RST {0}'.format (y * 8)

    assert instruction is not None

    print '0x{8:08X} {0} 0x{1:02X} x={2}, y={3}, z={4}, p={5}, q={6} ({7} bytes read)'.format (instruction, opcode, x, y, z, p, q, c, pc)
    return c


# Application entry point.
if __name__ == '__main__' :

    sms.readRom ('rom.sms')
    if sms.rom is None :
        exit (1)

    pc = 0
    while pc < len (sms.rom) :
        pc += decode (pc)
