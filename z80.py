
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

    # Increment the value of the register by 1.
    def inc(self) :
        self._v += 1
        if self._v > 0xFF : self._v = 0

    # Decrement the value of the register by 1.
    def dec(self) :
        self._v -= 1
        if self._v < 0 : self._v = 0xFF

##
# Simple class that represents a 16-bit data/address register. It contains
# two 8-bit register classes called lo and hi.
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

    # 16-bit increment by some value. Default is 1.
    def inc(self, a=1) :
        v = self.get ()
        v += a

        while v > 0xFFFF :
            v -= 0xFFFF

        self.set (v)

    # 16-bit decrement by some value. Default is 1.
    def dec(self, a=1) :
        v = self.get ()
        v -= a

        while v < 0 :
            v += 0xFFFF

        self.set (v)

    # Returns the bottom 8-bit register.
    def getLo(self) :
        return self._lo

    # Returns the top 8-bit register.
    def getHi(self) :
        return self._hi


class Z80(object) :

    def __init__(self) :

        self._pc = 0
        self._sp = 0
        self._ix = 0
        self._iy = 0
        self._iv = 0
        self._rc = 0

        # Registers
        self._b = 0
        self._c = 0
        self._d = 0
        self._e = 0
        self._a = 0
        self._f = 0

        # Shadow registers
        self._sb = 0
        self._sc = 0
        self._sd = 0
        self._se = 0
        self._sa = 0
        self._sf = 0

    # Returns the number of clock cycles.
    def run(self) :

        opcode = sms.readByte(self._pc)
        self._pc = (self._pc + 1) & 0xFFFF
        self._rc = (self._rc + 1) & 0xFF

        x = (opcode & 0xC0) >> 6
        y = (opcode & 0x38) >> 3
        z = (opcode & 0x7)
        p = y >> 1
        q = y & 0x1

        if x == 0 :

            if z == 0 :

                # NOP
                if y == 0 :
                    return 4

                # EX AF, AF'
                elif y == 1 :
                    self._a, self._sa = self._sa, self._a
                    self._f, self._sf = self._sf, self._f
                    return 4

                # DJNZ *
                elif y == 2 :

                    displacement = sms.readByte(self._pc)
                    self._pc = (self._pc + 1) & 0xFFFF
                    self._b = (self._b - 1) & 0xFF

                    if self._b != 0 :
                        # TODO displacement will be unsigned byte.
                        # TODO Need to convert to signed value.
                        self._pc = (self._pc + displacement) & 0xFFFF
                        return 13

                    return 8

                # JR *
                elif y == 3 :
                    displacement = sms.readByte(self._pc)
                    # TODO displacement will be unsigned byte.
                    # TODO Need to convert to signed value.
                    self._pc = (self._pc + 1) & 0xFFFF
                    self._pc = (self._pc + displacement) & 0xFFFF
                    return 12

                elif y in (4, 5, 6, 7) :

                    displacement = sms.readByte(self._pc)
                    self._pc = (self._pc + 1) & 0xFFFF

                    #if self._test_cc (y-4) :
                    #    self._pc.add (displacement)
                    #    return 12
                    return 7

            elif z == 1 :

                if q == 0 :

                    r1, r2 = [
                        (self._b, self._c),
                        (self._d, self._e),
                        (self._h, self._l),
                        (self._a, self._f)
                    ][p]                

                    r1 = sms.readByte (self._pc)
                    self._pc = (self._pc + 1) & 0xFFFF
                    r2 = sms.readByte (self._pc)
                    self._pc = (self._pc + 1) & 0xFFFF

                    return 10

                # ADD HL, rp
                elif q == 1 :
                    # self._table_rp(p).add (v)
                    # TODO Check overflow
                    return 11

            elif z == 2 :

                if q == 0 :

                    # LD (BC), A
                    if p == 0 :
                        d = self._registers[R_BC].get ()
                        v = self._registers[R_AF].getHi ().get ()
                        sms.writeByte(d, v)
                        return 7

                    # LD (DE), A
                    elif p == 1 :
                        d = self._registers[R_DE].get ()
                        v = self._registers[R_AF].getHi ().get ()
                        sms.writeByte(d, v)
                        return 7

                    # LD (**), HL
                    elif p == 2 :
                        d = sms.readWord(self._pc.get ())
                        self._pc.inc (2)
                        sms.writeWord(addr, self._registers[R_HL].get ())
                        return 16

                    # LD (**), A
                    elif p == 3 :
                        addr = sms.readWord(self._pc.get ())
                        self._pc.inc (2)
                        v = self._registers[R_AF].getHi ().get ()
                        sms.writeByte(addr, v)
                        return 13

                elif q == 1 :

                    # LD A, (BC)
                    if p == 0 :
                        addr = self._registers[R_BC].get ()
                        self._registers[R_AF].getHi ().set (sms.readByte (addr))
                        return 7

                    # LD A, (DE)
                    elif p == 1 :
                        addr = self._registers[R_DE].get ()
                        self._registers[R_AF].getHi ().set (sms.readByte (addr))
                        return 7

                    # LD HL, (**)
                    elif p == 2 :
                        addr = sms.readWord (self._pc.get ())
                        self._pc.inc (2)
                        self._registers[R_HL].set (sms.readWord (addr))
                        return 16

                    # LD A, (**)
                    elif p == 3 :
                        addr = sms.readWord (self._pc.get ())
                        self._pc.inc (2)
                        self._registers[R_AF].getHi ().set (sms.readByte (addr))
                        return 13

            elif z == 3 :

                # INC rp
                if q == 0 :
                    self._table_rp(p).inc ()
                    return 6

                # DEC rp
                elif q == 1 :
                    self._table_rp(p).dec ()
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
