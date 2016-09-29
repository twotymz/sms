
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

##
# Simple class that represents an 8-bit register.
class Register8(object) :

    def __init__(self) :
        self._v = 0

    def set(self, v) :
        self._v = v & 0xFF

    def get(self, v) :
        return self._v

    def inc(self) :
        self._v += 1
        if self._v > 0xFF : self._v = 0

    def dec(self) :
        self._v -= 1
        if self._v < 0 : self._v = 0xFF

##
# Simple class that represents a 16-bit data/address register or two 8-bit registers
class Register16(object) :

    def __init__(self) :
        self._lo = Register8 ()
        self._hi = Register8 ()

    # Get the 16-bit value of the register.
    def get(self) :
        return (self._hi.get () << 8) | self._lo.get ()

    # Set the 16-bit value of the register.
    def set(self, v) :
        self._hi.set (v & 0xFF00) >> 8)
        self._lo.set (v & 0x00FF)

    # 16-bit increment by 1.
    def inc(self) :
        v = self.get ()
        v += 1
        if v > 0xFFFF : v = 0
        self.set (v)

    # 16-bit decrement by 1.
    def dec(self) :
        v = self.get ()
        v -= 1
        if v < 0 : v = 0xFFFF
        self.set (v)

    # Get the bottom 8-bit value of the register.
    def getLo(self) :
        return self._lo.get ()

    # Set the bottom 8-bits of the register.
    def setLo(self, v) :
        self._lo.set (v)

    # Get the top 8-bit value of the register.
    def getHi(self) :
        return self._hi.get ()

    # Set the top 8-bits of the register.
    def setHi(self, v) :
        self._hi.set (v)


class Z80(object) :

    def __init__(self) :

        self._pc = Register16 ()
        self._sp = Register16 ()
        self._ix = Register16 ()
        self._iy = Register16 ()
        self._iv = Register8 ()
        self._rc = Register8 ()

        self._registers = [
            Register16 (),    # R_BC
            Register16 (),    # R_DE
            Register16 (),    # R_HL
            Register16 ()     # R_AF
        ]

        self._shadow_registers = [
            Register16 (),    # R_BC
            Register16 (),    # R_DE
            Register16 (),    # R_HL
            Register16 ()     # R_AF
        ]

    # Returns the number of clock cycles.
    def run(self, io) :

        opcode = io['readByte'](self._pc)
        self._rc += 1

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
                    displacement = io['readByte'](self._pc)

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
                    displacement = io['readByte'](self._pc)
                    self._pc += displacement
                    return 12

                # JR cc, *
                elif y in (4, 5, 6, 7) :
                    displacement = io['readByte'](self._pc)
                    if self._test_cc (y-4) :
                        self._pc += displacement
                        return 12

                    self._pc += 2
                    return 7

            elif z == 1 :

                # LD reg, **
                if q == 0 :
                    w = io['readWord'] (self._pc + 1)
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
                        io['writeByte'](self._regs[R_BC], self.reg_hi (R_AF))
                        self.pc += 1
                        return 7
                    # LD (DE), A
                    elif p == 1 :
                        io['writeByte'](self._regs[R_DE], self.reg_hi (R_AF))
                        self.pc += 1
                        return 7
                    # LD (**), HL
                    elif p == 2 :
                        addr = io['readWord'](self._pc + 1)
                        io['writeWord'](addr, self._regs[R_HL])
                        self.pc += 3
                        return 16
                    # LD (**), A
                    elif p == 3 :
                        addr = io['readWord'](self._pc + 1)
                        io['writeByte'](addr, self._reg_hi (R_AF))
                        self.pc += 3
                        return 13

                elif q == 1 :

                    # LD A, (BC)
                    if p == 0 :
                        self._reg_set_hi (R_AF, io['readByte'] (self._regs[R_BC]))
                        self._pc += 2
                        return 7
                    # LD A, (DE)
                    elif p == 1 :
                        self._reg_set_hi (R_AF, io['readByte'] (self._regs[R_DE]))
                        self._pc += 2
                        return 7
                    # LD HL, (**)
                    elif p == 2 :
                        addr = io['readWord'] (self._pc + 1)
                        self._regs[R_HL] = io['readWord'] (addr)
                        self._pc += 3
                        return 16
                    # LD A, (**)
                    elif p == 3 :
                        addr = io['readWord'] (self._pc + 1)
                        self._reg_set_hi (R_AF, io['readByte'] (addr))
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

        print 'Unhandled opcode {0:X}'.format (opcode)
        raise Exception
