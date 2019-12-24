
class Z80:

    def __init__(self, mapper):
        self.interrupts_enabled = True
        self.mapper = mapper

        # main registers
        self.af = 0
        self.bc = 0
        self.de = 0
        self.hl = 0

        # alternate registers
        self.af_ = 0
        self.bc_ = 0
        self.de_ = 0
        self.hl_ = 0

        # index registers
        self.ix = 0
        self.iy = 0
        self.sp = 0

        # other registers
        self.i = 0
        self.r = 0

        # program counter
        self.pc = 0

        self.h = {
            0x01: self._ld_bc,
            0x05: self._dec,
            0x06: self._ld_b,
            0x0D: self._dec,
            0x0E: self._ld_c,
            0x18: self._jr,
            0x20: self._jr,
            0x21: self._ld_hl,
            0x31: self._ld_sp,
            0x3E: self._ld_a,
            0x56: self._im,
            0x7E: self._ld_a,
            0xB3: self._otir,
            0xC3: self._jp,
            0xD3: self._out,
            0xF3: self._di_ei,
        }

    def run(self, instruction):

        print('-' * 20)
        print('{} 0x{:X} {}'.format(
            self.pc,
            instruction['opcode'],
            instruction['mnemonic']
        ))

        self.pc += instruction['bytes']
        self.h[instruction['opcode']](instruction)

        print('A: {:X} BC: {:04X} DE: {:04X} HL: {:04X} IX: {:04X} IY: {:04X}'.format(
            self.af & 0xF0 >> 8,
            self.bc,
            self.de,
            self.hl,
            self.ix,
            self.iy
        ))
        print("A': {:X} BC': {:04X} DE': {:04X} HL': {:04X} SP: {:04X}".format(
            self.af_ & 0xF0 >> 8,
            self.bc_,
            self.de_,
            self.hl_,
            self.sp
        ))
        print("FS: {} FZ: {} FHC: {} FP: {} FN: {} FC: {}".format(
            (self.af & 0x0080) >> 7,
            (self.af & 0x0040) >> 6,
            (self.af & 0x0010) >> 4,
            (self.af & 0x0004) >> 3,
            (self.af & 0x0002) >> 2,
            (self.af & 0x0001)
        ))

    ''' ======== Jump Instructions ======== '''

    def _jr(self, i):
        if i['opcode'] == 0x18:
            self.pc += i['displacement']

        elif i['opcode'] == 0x20:
            if self.af & 0x0040 == 0:
                self.pc += i['displacement']
        else:
            raise Exception('Bad Instruction')

    def _jp(self, i):
        if i['opcode'] == 0xC3:
            self.pc = i['immediate']
        else:
            raise Exception('Bad Instruction')

    ''' ======== Load Instructions ======== '''

    def _ld_a(self, i):
        if i['opcode'] == 0x3E:
            self.af = (self.af & 0x00FF) | (i['immediate'] & 0xFF) << 8
        elif i['opcode'] == 0x7E:
            self.af = (Self.af & 0x00FF) | (self.mapper.byte(self.hl) & 0xFF) << 8
        else:
            raise Exception('Bad Instruction')

    def _ld_b(self, i):
        if i['opcode'] == 0x06:
            self.bc = (self.bc & 0xFF) | (i['immediate'] & 0xFF) << 8
        else:
            raise Exception('Bad Instruction')

    def _ld_c(self, i):
        if i['opcode'] == 0x0E:
            self.bc = (self.bc & 0xFF00) | (i['immediate'] & 0xFF)
        else:
            raise Exception('Bad Instruction')

    def _ld_bc(self, i):
        if i['opcode'] == 0x01:
            self.bc = i['immediate']
        else:
            raise Exception('Bad Instruction')

    def _ld_hl(self, i):
        if i['opcode'] == 0x21:
            self.hl = i['immediate']
        else:
            raise Exception('Bad Instruction')

    def _ld_sp(self, i):
        if i['opcode'] == 0x31:
            self.sp = i['immediate']
        else:
            raise Exception('Bad Instruction')

    ''' ======== Decrement Instructions ======== '''

    def _dec(self, i):
        if i['opcode'] == 0x0D:
            c = self.bc & 0xFF
            c -= 1
            self._set_zero(1 if c == 0 else 0)
            self.bc = (self.bc & 0xFF00) | (c & 0xFF)
        elif i['opcode'] == 0x05:
            b = (self.bc & 0xFF00) >> 8
            b -= 1
            self._set_zero(1 if b == 0 else 0)
            self.bc = (self.bc & 0x00FF) | (b & 0xFF) << 8
        else:
            raise Exception('Bad Instruction')

    ''' ======== Unclassified Instructions ======== '''

    def _otir(self, i):
        b = (self.bc & 0xFF00) >> 8
        while b > 0:
            self.hl += 1
            b -= 1
            # TODO write what's stored at memory address (HL) to port C
            # (self.bc & 0x00FF)
        self.bc = (self.bc & 0x00FF) | (b & 0xFF) << 8

    def _out(self, i):
        if i['opcode'] == 0xD3:
            # TODO write what's at register A to port i['immediate']
            pass
        else:
            raise Exception('Bad Instruction')

    def _di_ei(self, i):
        self.interrupts_enabled = {
            0xF3: False,
            0xFB: True
        }[i['opcode']]

    def _im(self, i):
        # TODO ... set immediate mode properly
        pass

    ''' ======== Set Flags ======== '''

    def _set_zero(self, on_off):
        self._set_flag(6, 0x60, on_off)

    def _set_flag(self, bits, mask, on_off):
        flags = self.af = 0xFF
        if on_off:
            flags = flags | (1 << bits)
        else:
            flags = flags & ~(mask)

            self.af = (self.af & 0xFF00) | (flags & 0xFF)
