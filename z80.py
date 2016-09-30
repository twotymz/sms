
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

class Z80(object) :

    def __init__(self) :

        self._pc  = 0
        self._sph = 0
        self._spl = 0
        self._iv  = 0
        self._rc  = 0
        self._i   = 0
        self._r   = 0

        # Registers
        self._b = 0
        self._c = 0
        self._d = 0
        self._e = 0
        self._a = 0
        self._f = 0
        self._ixh = 0
        self._ixl = 0
        self._iyh = 0
        self._iyl = 0

        # Shadow registers
        self._sb = 0
        self._sc = 0
        self._sd = 0
        self._se = 0
        self._sa = 0
        self._sf = 0

    # Given two unsigned 8 bit values, make a 16 bit value.
    def _mw (self, h, l) : return h << 8 | l

    # Get the next byte at pc then incrementing pc.
    def _n (self) : b = sms.readByte (self._pc); self._pc = (self._pc + 1) & 0xFFFF; return b

    # Get the next word at pc incrementing pc.
    def _nn (self) : return self._mw (self._n (), self._n ())

    # Get a displacement value (-128 to 127)
    def _displacement(self) :
        b = self._n ()
        return b if b <= 127 else (256 - b) * -1

    # Shorthand to access register pairs.
    def _bc (self) : return self._mw (self._b, self._c)
    def _de (self) : return self._mw (self._b, self._c)
    def _hl (self) : return self._mw (self._h, self._l)
    def _ix (self) : return self._mw (self._ixh, self._ixl)
    def _iy (self) : return self._mw (self._iyh, self._iyl)
    def _sp (self) : return self._mw (self._sph, self._spl)

    def _ld_a_a (self) : self._a = self._a
    def _ld_a_b (self) : self._a = self._b
    def _ld_a_c (self) : self._a = self._c
    def _ld_a_d (self) : self._a = self._d
    def _ld_a_e (self) : self._a = self._e
    def _ld_a_h (self) : self._a = self._h
    def _ld_a_l (self) : self._a = self._l
    def _ld_a_i (self) : self._a = self._i
    def _ld_a_r (self) : self._a = self._r
    def _ld_a_ixh (self) : self._a = self._ixh
    def _ld_a_ixl (self) : self._a = self._ixl
    def _ld_a_iyh (self) : self._a = self._iyh
    def _ld_a_iyl (self) : self._a = self._iyl
    def _ld_a_m_bc (self) : self._a = sms.readByte (self._bc ())
    def _ld_a_m_de (self) : self._a = sms.readByte (self._de ())
    def _ld_a_m_hl (self) : self._a = sms.readByte (self._hl ())
    def _ld_a_m_ixn (self) : pass
    def _ld_a_m_iyn (self) : pass
    def _ld_a_n (self) : self._a = self._n ()
    def _ld_a_m_nn (self) : self._a = sms.readByte (self._nn ())
    def _ld_b_a (self) : self._b = self._a
    def _ld_b_b (self) : self._b = self._b
    def _ld_b_c (self) : self._b = self._c
    def _ld_b_d (self) : self._b = self._d
    def _ld_b_e (self) : self._b = self._e
    def _ld_b_h (self) : self._b = self._h
    def _ld_b_l (self) : self._b = self._l
    def _ld_b_ixh (self) : self._b = self._ixh
    def _ld_b_ixl (self) : self._b = self._ixl
    def _ld_b_iyh (self) : self._b = self._iyh
    def _ld_b_iyl (self) : self._b = self._iyl
    def _ld_b_m_hl (self) : self._b = sms.readByte (self._hl ())
    def _ld_b_m_ixn (self) : pass
    def _ld_b_m_iyn (self) : pass
    def _ld_b_n (self) : self._b = self._n ()
    def _ld_c_a (self) : self._c = self._a
    def _ld_c_b (self) : self._c = self._b
    def _ld_c_c (self) : self._c = self._c
    def _ld_c_d (self) : self._c = self._d
    def _ld_c_e (self) : self._c = self._e
    def _ld_c_h (self) : self._c = self._h
    def _ld_c_l (self) : self._c = self._l
    def _ld_c_ixh (self) : self._c = self._ixh
    def _ld_c_ixl (self) : self._c = self._ixl
    def _ld_c_iyh (self) : self._c = self._iyh
    def _ld_c_iyl (self) : self._c = self._iyl
    def _ld_c_m_hl (self) : self._c = sms.readByte (self._hl ())
    def _ld_c_m_ixn (self) : pass
    def _ld_c_m_iyn (self) : pass
    def _ld_c_n (self) : self._c = self._n ()
    def _ld_d_a (self) : self._d = self._a
    def _ld_d_b (self) : self._d = self._b
    def _ld_d_c (self) : self._d = self._c
    def _ld_d_d (self) : self._d = self._d
    def _ld_d_e (self) : self._d = self._e
    def _ld_d_h (self) : self._d = self._h
    def _ld_d_l (self) : self._d = self._l
    def _ld_d_ixh (self) : self._d = self._ixh
    def _ld_d_ixl (self) : self._d = self._ixl
    def _ld_d_iyh (self) : self._d = self._iyh
    def _ld_d_iyl (self) : self._d = self._iyl
    def _ld_d_m_hl (self) : self._d = sms.readByte (self._hl ())
    def _ld_d_m_ixn (self) : pass
    def _ld_d_m_iyn (self) : pass
    def _ld_d_n (self) : self._d = self._n ()
    def _ld_e_a (self) : self._e = self._a
    def _ld_e_b (self) : self._e = self._b
    def _ld_e_c (self) : self._e = self._c
    def _ld_e_d (self) : self._e = self._d
    def _ld_e_e (self) : self._e = self._e
    def _ld_e_h (self) : self._e = self._h
    def _ld_e_l (self) : self._e = self._l
    def _ld_e_ixh (self) : self._e = self._ixh
    def _ld_e_ixl (self) : self._e = self._ixl
    def _ld_e_iyh (self) : self._e = self._iyh
    def _ld_e_iyl (self) : self._e = self._iyl
    def _ld_e_m_hl (self) : self._e = sms.readByte (self._hl ())
    def _ld_e_m_ixn (self) : pass
    def _ld_e_m_iyn (self) : pass
    def _ld_e_n (self) : self._e = self._n ()
    def _ld_h_a (self) : self._h = self._a
    def _ld_h_b (self) : self._h = self._b
    def _ld_h_c (self) : self._h = self._c
    def _ld_h_d (self) : self._h = self._d
    def _ld_h_e (self) : self._h = self._e
    def _ld_h_h (self) : self._h = self._h
    def _ld_h_l (self) : self._h = self._l
    def _ld_h_ixh (self) : self._h = self._ixh
    def _ld_h_ixl (self) : self._h = self._ixl
    def _ld_h_iyh (self) : self._h = self._iyh
    def _ld_h_iyl (self) : self._h = self._iyl
    def _ld_h_m_hl (self) : self._h = sms.readByte (self._hl ())
    def _ld_h_m_ixn (self) : pass
    def _ld_h_m_iyn (self) : pass
    def _ld_h_n (self) : self._h = self._n ()
    def _ld_l_a (self) : self._l = self._a
    def _ld_l_b (self) : self._l = self._b
    def _ld_l_c (self) : self._l = self._c
    def _ld_l_d (self) : self._l = self._d
    def _ld_l_e (self) : self._l = self._e
    def _ld_l_h (self) : self._l = self._h
    def _ld_l_l (self) : self._l = self._l
    def _ld_l_ixh (self) : self._l = self._ixh
    def _ld_l_ixl (self) : self._l = self._ixl
    def _ld_l_iyh (self) : self._l = self._iyh
    def _ld_l_iyl (self) : self._l = self._iyl
    def _ld_l_m_hl (self) : self._l = sms.readByte (self._hl ())
    def _ld_l_m_ixn (self) : pass
    def _ld_l_m_iyn (self) : pass
    def _ld_l_n (self) : self._l = self._n ()
    def _ld_i_a (self) : self._i = self._a      # TODO flags
    def _ld_r_a (self) : self._r = self._a      # TODO flags
    def _ld_ixh_a (self) : self._ixh = self._a
    def _ld_ixh_b (self) : self._ixh = self._b
    def _ld_ixh_c (self) : self._ixh = self._c
    def _ld_ixh_d (self) : self._ixh = self._d
    def _ld_ixh_e (self) : self._ixh = self._e
    def _ld_ixh_h (self) : self._ixh = self._h
    def _ld_ixh_l (self) : self._ixh = self._l
    def _ld_ixh_ixh (self) : pass   # nop that lasts 9 t-states
    def _ld_ixh_ixl (self) : self._ixh = self._ixl
    def _ld_ixh_n (self) : self._ixh = self._n ()
    def _ld_ixl_a (self) : self._ixl = self._a
    def _ld_ixl_b (self) : self._ixl = self._b
    def _ld_ixl_c (self) : self._ixl = self._c
    def _ld_ixl_d (self) : self._ixl = self._d
    def _ld_ixl_e (self) : self._ixl = self._e
    def _ld_ixl_h (self) : self._ixl = self._h
    def _ld_ixl_l (self) : self._ixl = self._l
    def _ld_ixl_ixh (self) : self._ixl = self._ixh
    def _ld_ixl_ixl (self) : pass   # nop that lasts 9 t-states
    def _ld_ixl_n (self) : self._ixl = self._n()
    def _ld_iyh_a (self) : self._iyh = self._a
    def _ld_iyh_b (self) : self._iyh = self._b
    def _ld_iyh_c (self) : self._iyh = self._c
    def _ld_iyh_d (self) : self._iyh = self._d
    def _ld_iyh_e (self) : self._iyh = self._e
    def _ld_iyh_h (self) : self._iyh = self._h
    def _ld_iyh_l (self) : self._iyh = self._l
    def _ld_iyh_iyh (self) : pass   # nop that lasts 9 t-states
    def _ld_iyh_iyl (self) : self._iyh = self._iyl
    def _ld_iyh_n (self) : self._iyh = self._n()
    def _ld_iyl_a (self) : self._iyl = self._a
    def _ld_iyl_b (self) : self._iyl = self._b
    def _ld_iyl_c (self) : self._iyl = self._c
    def _ld_iyl_d (self) : self._iyl = self._d
    def _ld_iyl_e (self) : self._iyl = self._e
    def _ld_iyl_h (self) : self._iyl = self._h
    def _ld_iyl_l (self) : self._iyl = self._l
    def _ld_iyl_iyh (self) : self._iyl = self._iyh
    def _ld_iyl_iyl (self) : pass   # nop that lasts 9 t-states
    def _ld_iyl_n (self) : self._iyl = self._n()
    def _ld_bc_nn (self) : self._b = self._n (); self._c = self._n ()
    def _ld_bc_m_nn (self) : a = self._nn(); self._b = sms.readByte (a); self._c = sms.readByte (a+1)
    def _ld_de_nn (self) : self._d = self._n (); self._e = self._n ()
    def _ld_de_m_nn (self) : a = self._nn(); self._d = sms.readByte (a); self._e = sms.readByte (a+1)
    def _ld_hl_nn (self) : self._h = self._n (); self._l = self._n ()
    def _ld_hl_m_nn (self) : a = self._nn(); self._h = sms.readByte (a); self._l = sms.readByte (a+1)
    def _ld_sp_hl (self) : self._sph = self._h; self._spl = self._l
    def _ld_sp_ix (self) : self._sph = self._ixh; self._spl = self._ixl
    def _ld_sp_iy (self) : self._sph = self._iyh; self._spl = self._iyl
    def _ld_sp_nn (self) : self._sph = self._n (); self._spl = self._n ()
    def _ld_sp_m_nn (self) : a = self._nn(); self._sph = sms.readByte (a); self._spl = sms.readByte (a+1)
    def _ld_ix_nn (self) : self._ixh = self._n(); self._ixl = self._n ()
    def _ld_ix_m_nn (self) : a = self._nn (); self._ixh = sms.readByte (a); self._ixl = sms.readByte (a+1)
    def _ld_iy_nn (self) : self._iyh = self._n(); self._iyl = self._n ()
    def _ld_iy_m_nn (self) : a = self._nn(); self._iyh = sms.readByte (a); self._iyl = sms.readByte (a+1)
    def _ld_m_bc_a (self) : sms.writeByte (self._bc (), self._a)
    def _ld_m_de_a (self) : sms.writeByte (self._de (), self._a)
    def _ld_m_hl_a (self) : sms.writeByte (self._hl (), self._a)
    def _ld_m_hl_b (self) : sms.writeByte (self._hl (), self._b)
    def _ld_m_hl_c (self) : sms.writeByte (self._hl (), self._c)
    def _ld_m_hl_d (self) : sms.writeByte (self._hl (), self._d)
    def _ld_m_hl_e (self) : sms.writeByte (self._hl (), self._e)
    def _ld_m_hl_h (self) : sms.writeByte (self._hl (), self._h)
    def _ld_m_hl_l (self) : sms.writeByte (self._hl (), self._l)
    def _ld_m_hl_n (self) : sms.writeByte (self._hl (), self._n())
    def _ld_m_nn_a (self) : sms.writeByte (self._mw (self._n (), self._n()), self._a)
    def _ld_m_nn_bc (self) : a = self._nn(); sms.writeByte (a, self._b); sms.writeByte (a+1, self._c)
    def _ld_m_nn_de (self) : a = self._nn(); sms.writeByte (a, self._d); sms.writeByte (a+1, self._e)
    def _ld_m_nn_hl (self) : a = self._nn(); sms.writeByte (a, self._h); sms.writeByte (a+1, self._l)
    def _ld_m_nn_sp (self) : a = self._nn(); sms.writeByte (a, self._sph); sms.writeByte (a+1, self._spl)
    def _ld_m_nn_ix (self) : a = self._nn(); sms.writeByte (a, self._ixh); sms.writeByte (a+1, self._ixl)
    def _ld_m_nn_iy (self) : a = self._nn(); sms.writeByte (a, self._iyh); sms.writeByte (a+1, self._iyl)

    def _jp (self) : pass
    def _jp_m_hl (self) : pass
    def _jp_m_ix (self) : pass
    def _jp_m_iy (self) : pass
    def _jp_nz (self) : pass
    def _jp_z (self) : pass
    def _jp_nc (self) : pass
    def _jp_po (self) : pass
    def _jp_pe (self) : pass
    def _jp_p (self) : pass
    def _jp_m (self) : pass
    def _jr (self) : d = self._displacement (); self._pc = (self._pc + d) & 0xFFFF
    def _jr_nz (self) : pass
    def _jr_z (self) : pass
    def _jr_nc (self) : pass
    def _jr_c (self) : pass
    def _djnz (self) : pass

    def _inc_a (self) : pass
    def _inc_b (self) : pass
    def _inc_c (self) : pass
    def _inc_d (self) : pass
    def _inc_e (self) : pass
    def _inc_h (self) : pass
    def _inc_l (self) : pass
    def _inc_ixh (self) : pass
    def _inc_ixl (self) : pass
    def _inc_m_hl (self) : pass
    def _inc_m_ixn (self) : pass
    def _inc_m_iyn (self) : pass
    def _inc_bc (self) : pass
    def _inc_de (self) : pass
    def _inc_hl (self) : pass
    def _inc_ix (self) : pass
    def _inc_iy (self) : pass
    def _inc_sp (self) : pass

    def _dec_a (self) : pass
    def _dec_b (self) : pass
    def _dec_c (self) : pass
    def _dec_d (self) : pass
    def _dec_e (self) : pass
    def _dec_h (self) : pass
    def _dec_l (self) : pass
    def _dec_ixh (self) : pass
    def _dec_ixl (self) : pass
    def _dec_m_hl (self) : pass
    def _dec_m_ixn (self) : pass
    def _dec_m_iyn (self) : pass
    def _dec_bc (self) : pass
    def _dec_de (self) : pass
    def _dec_hl (self) : pass
    def _dec_ix (self) : pass
    def _dec_iy (self) : pass
    def _dec_sp (self) : pass

    

    def _nop (self) : pass
    def _halt (self) : pass

    def _ex_af_af (self) : self._a, self._sa = self._sa, self._a; self._f, self._sf = self._sf, self._f

    # Returns the number of clock cycles.
    def run(self) :

        opcode = self._n ()
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
                    self._ex_af_af ()
                    return 4

                # DJNZ *
                elif y == 2 :
                    d = self._displacement ()
                    self._b = (self._b - 1) & 0xFF
                    if self._b != 0 :
                        self._pc = (self._pc + d) & 0xFFFF
                        return 13
                    return 8

                # JR *
                elif y == 3 :
                    self._pc = (self._pc + self._displacement ()) & 0xFFFF
                    return 12

                elif y in (4, 5, 6, 7) :
                    #displacement = self._n ()
                    #if self._test_cc (y-4) :
                    #    self._pc.add (displacement)
                    #    return 12
                    return 7

            elif z == 1 :

                if q == 0 :
                    if p == 0 :
                        self._ld_bc_nn ()
                    elif p == 1 :
                        self._ld_de_nn ()
                    elif p == 2 :
                        self._ld_hl_nn ()
                    elif p == 3 :
                        self._ld_sp_nn ()
                    return 10

                # ADD HL, rp
                elif q == 1 :
                    # TODO
                    return 11

            elif z == 2 :

                if q == 0 :

                    # LD (BC), A
                    if p == 0 :
                        self._ld_m_bc_a ()
                        return 7

                    # LD (DE), A
                    elif p == 1 :
                        self._ld_m_de_a ()
                        return 7

                    # LD (**), HL
                    elif p == 2 :
                        self._ld_m_nn_hl ()
                        return 16

                    # LD (**), A
                    elif p == 3 :
                        self._ld_m_nn_a ()
                        return 13

                elif q == 1 :

                    # LD A, (BC)
                    if p == 0 :
                        self._ld_a_m_bc ()
                        return 7

                    # LD A, (DE)
                    elif p == 1 :
                        self._ld_a_m_de ()
                        return 7

                    # LD HL, (**)
                    elif p == 2 :
                        self._ld_hl_m_nn ()
                        return 16

                    # LD A, (**)
                    elif p == 3 :
                        self._ld_a_m_nn ()
                        return 13

            elif z == 3 :

                # INC rp
                if q == 0 :
                    #self._table_rp(p).inc ()
                    return 6

                # DEC rp
                elif q == 1 :
                    #self._table_rp(p).dec ()
                    return 6

            # INC r
            elif z == 4 :
                # TODO
                #self._inc_pc ()
                return 4

            # DEC r
            elif z == 5 :
                # TODO
                #self._inc_pc ()
                return 4

            # LD r, *
            elif z == 6 :
                if y == 0 :
                    self._ld_b_n ()
                elif y == 1 :
                    self._ld_c_n ()
                elif y == 2 :
                    self._ld_d_n ()
                elif y == 3 :
                    self._ld_e_n ()
                elif y == 4 :
                    self._ld_h_n ()
                elif y == 5 :
                    self._ld_l_n ()
                elif y == 6 :
                    self._ld_m_hl_n ()
                elif y == 7 :
                    self._ld_a_n ()
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

                return 4

        print 'Unhandled opcode {0:X}'.format (opcode)
        raise Exception
