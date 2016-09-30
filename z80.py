
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


    def _ld_a_a (self) : self._a = self._a
    def _ld_a_b (self) : self._a = self._b
    def _ld_a_c (self) : self._a = self._c
    def _ld_a_d (self) : self._a = self._d
    def _ld_a_e (self) : self._a = self._e
    def _ld_a_h (self) : self._a = self._h
    def _ld_a_l (self) : self._a = self._l
    def _ld_a_i (self) : pass
    def _ld_a_r (self) : pass
    def _ld_a_ixh (self) : pass
    def _ld_a_ixl (self) : pass
    def _ld_a_iyh (self) : pass
    def _ld_a_iyl (self) : pass
    def _ld_a_m_bc (self) : pass
    def _ld_a_m_de (self) : pass
    def _ld_a_m_hl (self) : pass
    def _ld_a_m_ixn (self) : pass
    def _ld_a_m_iyn (self) : pass
    def _ld_a_n (self) : pass
    def _ld_a_m_nn (self) : pass
    def _ld_b_a (self) : self._b = self._a
    def _ld_b_b (self) : self._b = self._b
    def _ld_b_c (self) : self._c = self._c
    def _ld_b_d (self) : self._d = self._d
    def _ld_b_e (self) : self._e = self._e
    def _ld_b_h (self) : self._h = self._h
    def _ld_b_l (self) : self._l = self._l
    def _ld_b_ixh (self) : pass
    def _ld_b_ixl (self) : pass
    def _ld_b_iyh (self) : pass
    def _ld_b_iyl (self) : pass
    def _ld_b_m_hl (self) : pass
    def _ld_b_m_ixn (self) : pass
    def _ld_b_m_iyn (self) : pass
    def _ld_b_n (self) : pass
    def _ld_c_a (self) : self._c = self._a
    def _ld_c_b (self) : self._c = self._b
    def _ld_c_c (self) : self._c = self._c
    def _ld_c_d (self) : self._c = self._d
    def _ld_c_e (self) : self._c = self._e
    def _ld_c_h (self) : self._c = self._h
    def _ld_c_l (self) : self._c = self._l
    def _ld_c_ixh (self) : pass
    def _ld_c_ixl (self) : pass
    def _ld_c_iyh (self) : pass
    def _ld_c_iyl (self) : pass
    def _ld_c_m_hl (self) : pass
    def _ld_c_m_ixn (self) : pass
    def _ld_c_m_iyn (self) : pass
    def _ld_c_n (self) : pass
    def _ld_d_a (self) : self._d = self._a
    def _ld_d_b (self) : self._d = self._b
    def _ld_d_c (self) : self._d = self._c
    def _ld_d_d (self) : self._d = self._d
    def _ld_d_e (self) : self._d = self._e
    def _ld_d_h (self) : self._d = self._h
    def _ld_d_l (self) : self._d = self._l
    def _ld_d_ixh (self) : pass
    def _ld_d_ixl (self) : pass
    def _ld_d_iyh (self) : pass
    def _ld_d_iyl (self) : pass
    def _ld_d_m_hl (self) : pass
    def _ld_d_m_ixn (self) : pass
    def _ld_d_m_iyn (self) : pass
    def _ld_d_n (self) : pass
    def _ld_e_a (self) : self._e = self._a
    def _ld_e_b (self) : self._e = self._b
    def _ld_e_c (self) : self._e = self._c
    def _ld_e_d (self) : self._e = self._d
    def _ld_e_e (self) : self._e = self._e
    def _ld_e_h (self) : self._e = self._h
    def _ld_e_l (self) : self._e = self._l
    def _ld_e_ixh (self) : pass
    def _ld_e_ixl (self) : pass
    def _ld_e_iyh (self) : pass
    def _ld_e_iyl (self) : pass
    def _ld_e_m_hl (self) : pass
    def _ld_e_m_ixn (self) : pass
    def _ld_e_m_iyn (self) : pass
    def _ld_e_n (self) : pass
    def _ld_h_a (self) : self._h = self._a
    def _ld_h_b (self) : self._h = self._b
    def _ld_h_c (self) : self._h = self._c
    def _ld_h_d (self) : self._h = self._d
    def _ld_h_e (self) : self._h = self._e
    def _ld_h_h (self) : self._h = self._h
    def _ld_h_l (self) : self._h = self._l
    def _ld_h_ixh (self) : pass
    def _ld_h_ixl (self) : pass
    def _ld_h_iyh (self) : pass
    def _ld_h_iyl (self) : pass
    def _ld_h_m_hl (self) : pass
    def _ld_h_m_ixn (self) : pass
    def _ld_h_m_iyn (self) : pass
    def _ld_h_n (self) : pass
    def _ld_l_a (self) : self._l = self._a
    def _ld_l_b (self) : self._l = self._b
    def _ld_l_c (self) : self._l = self._c
    def _ld_l_d (self) : self._l = self._d
    def _ld_l_e (self) : self._l = self._e
    def _ld_l_h (self) : self._l = self._h
    def _ld_l_l (self) : self._l = self._l
    def _ld_l_ixh (self) : pass
    def _ld_l_ixl (self) : pass
    def _ld_l_iyh (self) : pass
    def _ld_l_iyl (self) : pass
    def _ld_l_m_hl (self) : pass
    def _ld_l_m_ixn (self) : pass
    def _ld_l_m_iyn (self) : pass
    def _ld_l_n (self) : pass
    def _ld_i_a (self) : pass
    def _ld_r_a (self) : pass
    def _ld_sp_hl (self) : pass
    def _ld_sp_ix (self) : pass
    def _ld_sp_iy (self) : pass
    def _ld_m_bc_a (self) : pass
    def _ld_m_de_a (self) : pass
    def _ld_m_hl_a (self) : pass
    def _ld_hl_b (self) : pass
    def _ld_hl_c (self) : pass
    def _ld_hl_d (self) : pass
    def _ld_hl_e (self) : pass
    def _ld_hl_h (self) : pass
    def _ld_hl_l (self) : pass
    def _ld_m_nn_a (self) : pass
    def _ld_m_nn_bc (self) : pass
    def _ld_m_nn_de (self) : pass
    def _ld_m_nn_hl (self) : pass
    def _ld_m_nn_sp (self) : pass
    def _ld_m_nn_ix (self) : pass
    def _ld_m_nn_iy (self) : pass

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
                    if p == 0 :
                        self._b = sms.readByte (self._pc)
                        self._pc = (self._pc + 1) & 0xFFFF
                        self._c = sms.readByte (self._pc)
                        self._pc = (self._pc + 1) & 0xFFFF
                    elif p == 1 :
                        self._d = sms.readByte (self._pc)
                        self._pc = (self._pc + 1) & 0xFFFF
                        self._e = sms.readByte (self._pc)
                        self._pc = (self._pc + 1) & 0xFFFF
                    elif p == 2 :
                        self._h = sms.readByte (self._pc)
                        self._pc = (self._pc + 1) & 0xFFFF
                        self._l = sms.readByte (self._pc)
                        self._pc = (self._pc + 1) & 0xFFFF
                    elif p == 3 :
                        self._a = sms.readByte (self._pc)
                        self._pc = (self._pc + 1) & 0xFFFF
                        self._f = sms.readByte (self._pc)
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
                        addr = self._b << 8 | self._c
                        sms.writeByte(addr, self._a)
                        return 7

                    # LD (DE), A
                    elif p == 1 :
                        addr = self._d << 8 | self._e
                        sms.writeByte(addr, self._a)
                        return 7

                    # LD (**), HL
                    elif p == 2 :
                        addr = sms.readByte (self._pc) << 8
                        self._pc = (self._pc + 1) & 0xFFFF
                        addr = addr | sms.readByte (self._pc)
                        self._pc = (self._pc + 1) & 0xFFFF
                        sms.writeByte (addr, self._h)
                        sms.writeByte (addr + 1, self._l)
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
                        addr = self._b << 8 | self._c
                        self._a = sms.readByte (addr)
                        return 7

                    # LD A, (DE)
                    elif p == 1 :
                        addr = self._d << 8 | self._e
                        self._a = sms.readByte (addr)
                        return 7

                    # LD HL, (**)
                    elif p == 2 :
                        addr = sms.readByte (self._pc) << 8
                        self._pc = (self._pc + 1) & 0xFFFF
                        addr = addr | sms.readByte (self._pc)
                        self._pc = (self._pc + 1) & 0xFFFF
                        self._h = sms.readByte (addr)
                        self._l = sms.readByte (addr + 1)
                        return 16

                    # LD A, (**)
                    elif p == 3 :
                        addr = sms.readByte (self._pc) << 8
                        self._pc = (self._pc + 1) & 0xFFFF
                        addr = addr | sms.readByte (self._pc)
                        self._pc = (self._pc + 1) & 0xFFFF
                        self._a = sms.readByte (addr)
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
                if y == 0 :
                    self._b = sms.readByte (self._pc)
                elif y == 1 :
                    self._c = sms.readByte (self._pc)
                elif y == 2 :
                    self._d = sms.readByte (self._pc)
                elif y == 3 :
                    self._e = sms.readByte (self._pc)
                elif y == 4 :
                    self._h = sms.readByte (self._pc)
                elif y == 5 :
                    self._l = sms.readByte (self._pc)
                elif y == 6 :
                    # TODO
                    pass
                elif y == 7 :
                    self._a = sms.readByte (self._pc)

                self._pc = (self._pc + 1) & 0xFFFF
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

                self._pc = (self._pc + 1) & 0xFFFF
                return 4

        print 'Unhandled opcode {0:X}'.format (opcode)
        raise Exception
