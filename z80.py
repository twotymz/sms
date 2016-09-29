
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
            Register16AF),    # R_BC
            Register16 (),    # R_D
            Register16 (),    # R_HL
            Register16 ()     # R_AF
        ]

    def _table_rp (self, p) :
        return [
            self._registers[R_BC],
            self._registers[R_DE],
            self._registers[R_HL],
            self._sp
        ][p]

    def _table_r (self, p) :
        return [
            self._registers[R_BC].getHi (),
            self._registers[R_BC].getLo (),
            self._registers[R_DE].getHi (),
            self._registers[R_DE].getLo (),
            self._registers[R_HL].getHi (),
            self._registers[R_HL].getLo (),
            None,
            self._registers[R_AF].getHi ()
        ][p]

    # Returns the number of clock cycles.
    def run(self) :

        opcode = sms.readByte(self._pc.get ())
        self._pc.inc ()
        self._rc.inc ()

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
                    t = self._registers[R_AF].get ()
                    self._registers[R_AF].set (self._shadow_registers[R_AF].get ())
                    self._shadow_registers[R_AF].set (t)
                    return 4

                # DJNZ *
                elif y == 2 :

                    displacement = sms.readByte(self._pc.get ())
                    self._pc.inc ()

                    b = self._registers[R_BC].getHi()
                    b.dec ()

                    if b.get () != 0 :
                        # TODO displacement will be unsigned byte.
                        # TODO Need to convert to signed value.
                        self._pc.add (displacement)
                        return 13

                    return 8

                # JR *
                elif y == 3 :
                    displacement = sms.readByte(self._pc.get ())
                    self._pc.inc ()
                    self._pc.add (displacement)
                    return 12

                # JR cc, *
                elif y in (4, 5, 6, 7) :
                    displacement = sms.readByte(self._pc.get ())
                    self._pc.inc ()
                    if self._test_cc (y-4) :
                        self._pc.add (displacement)
                        return 12
                    return 7

            elif z == 1 :

                # LD reg, **
                if q == 0 :
                    w = sms.readWord (self._pc.get ())
                    self._pc.inc (2)
                    self._table_rp (p).set (w)
                    return 10

                # ADD HL, rp
                elif q == 1 :
                    self._table_rp(p).add (v)
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
