
import sms

R_BC = 0
R_DE = 1
R_HL = 2
R_AF = 3

F_C = 0
F_N = 1
F_P = 2
F_H = 4
F_Z = 6
F_S = 7

class CPU(object) :


    def __init__(self) :
        self._pc = 0
        self._sp = 0
        self._regs = [0, 0, 0, 0]
        self._alt_regs = [0, 0, 0, 0]


    def _test_cc(self, cc) :
        return 0


    def _reg_lo(self, r) :
        return self._regs[r] & 0xFF


    def _reg_hi(self, r) :
        return self._regs[r] >> 8


    def _reg_set_lo(self, r, v) :
        self._regs[r] = (self._regs[r] & 0xFF00) | (v & 0xFF)


    def _reg_set_hi(self, r, v) :
        self._regs[r] = (self._regs[r] & 0x00FF) | ((v & 0xFF) << 8)


    # Returns the number of clock cycles.
    def run(self) :

        opcode = sms.readByte (self._pc)

        x = (opcode & 0xC0) >> 6
        y = (opcode & 0x38) >> 3
        z = (opcode & 0x7)
        p = y >> 1
        q = y & 0x1

        if x == 0 :

            if z == 0 :

                # NOP
                if y == 0 :
                    self._pc += 1
                    return 4

                # EX AF, AF'
                elif y == 1 :
                    t = self._regs[R_AF]
                    self._regs[R_AF] = self._shadow_regs[R_AF]
                    self._alt_regs[R_AF] = t
                    self._pc += 1
                    return 4

                # DJNZ *
                elif y == 2 :
                    displacement = sms.readByte(self._pc)

                    b = sef._reg_hi (R_BC)
                    b = b - 1
                    if b < 0 : b = 255
                    self._reg_set_hi (R_BC, b)

                    if b != 0 :
                        self._pc += displacement
                        return 13

                    self._pc += 2
                    return 8

                # JR *
                elif y == 3 :
                    displacement = sms.readByte(self._pc)
                    self._pc += displacement
                    return 12

                # JR cc, *
                elif y in (4, 5, 6, 7) :
                    displacement = sms.readByte(self._pc)
                    if self._test_cc (y-4) :
                        self._pc += displacement
                        return 12

                    self._pc += 2
                    return 7

            elif z == 1 :

                # LD reg, **
                if q == 0 :
                    w = sms.readWord (self._pc + 1)
                    if p == 3 :
                        self._sp = w
                    else :
                        self._regs[p] = w
                    self._pc += 3
                    return 10
                # ADD HL, rp
                elif q == 1 :

                    if p == 3 :
                        v = self._sp
                    else :
                        v = self._regs[p]

                    r = self._regs[R_HL] + v

                    # TODO Check overflow

                    self._regs[R_HL] = r
                    self._pc += 1
                    return 11

            elif z == 2 :

                if q == 0 :

                    # LD (BC), A
                    if p == 0 :
                        sms.writeByte (self._regs[R_BC], self.reg_hi (R_AF))
                        self.pc += 1
                        return 7
                    # LD (DE), A
                    elif p == 1 :
                        sms.writeByte (self._regs[R_DE], self.reg_hi (R_AF))
                        self.pc += 1
                        return 7
                    # LD (**), HL
                    elif p == 2 :
                        addr = sms.readWord (self._pc + 1)
                        sms.writeWord (addr, self._regs[R_HL])
                        self.pc += 3
                        return 16
                    # LD (**), A
                    elif p == 3 :
                        addr = sms.readWord (self._pc + 1)
                        sms.writeByte (addr, self._reg_hi (R_AF))
                        self.pc += 3
                        return 13

                elif q == 1 :

                    # LD A, (BC)
                    if p == 0 :
                        self._reg_set_hi (R_AF, sms.readByte (self._regs[R_BC]))
                        self._pc += 2
                        return 7
                    # LD A, (DE)
                    elif p == 1 :
                        self._reg_set_hi (R_AF, sms.readByte (self._regs[R_DE]))
                        self._pc += 2
                        return 7
                    # LD HL, (**)
                    elif p == 2 :
                        addr = sms.readWord (self._pc + 1)
                        self._regs[R_HL] = sms.readWord (addr)
                        self._pc += 3
                        return 16
                    # LD A, (**)
                    elif p == 3 :
                        addr = sms.readWord (self._pc + 1)
                        self._reg_set_hi (R_AF, sms.readByte (addr))
                        self._pc += 3
                        return 13

            elif z == 3 :

                # INC rp
                if q == 0 :
                    if p == 3 :
                        self._sp += 1
                    else :
                        self._regs[p] += 1
                    self._pc += 1
                    return 6

                # DEC rp
                elif q == 1 :
                    if p == 3 :
                        self._sp -= 1
                    else :
                        self._regs[p] -= 1

                    self._pc += 1
                    return 6

            # INC r
            elif z == 4 :
                # TODO
                self._pc += 1
                return 4

            # DEC r
            elif z == 5 :
                # TODO
                self._pc += 1
                return 4

            # LD r, *
            elif z == 6 :
                # TODO
                self._pc += 2
                return 7

            elif z == 7 :

                # RLCA
                if y == 0 :
                    pass

                # RRCA
                elif y == 1 :
                    pass

                # RLA
                elif y == 2 :
                    pass

                # RRA
                elif y == 3 :
                    pass

                # DAA
                elif y == 4 :
                    pass

                # CPL
                elif y == 5 :
                    pass

                # SCF
                elif y == 6 :
                    pass

                # CCF
                elif y == 7 :
                    pass

                self._pc += 1
                return 4




    raise Exception
