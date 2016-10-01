
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

        self._opcodes = [
            self._nop,
            self._ld_bc_nn,
            self._ld_m_bc_a,
            self._inc_bc,
            self._inc_b,
            self._dec_b,
            self._ld_b_n,
            self._rlca,
            self._ex_af_af,
            self._add_hl_bc,
            self._ld_a_m_bc,
            self._dec_bc,
            self._inc_c,
            self._dec_c,
            self._ld_c_n,
            self._rrca,
            self._djnz,
            self._ld_de_nn,
            self._ld_m_de_a,
            self._inc_de,
            self._inc_d,
            self._dec_d,
            self._ld_d_n,
            self._rla,
            self._jr,
            self._add_hl_de,
            self._ld_a_m_de,
            self._dec_de,
            self._inc_e,
            self._dec_e,
            self._ld_e_n,
            self._rra,
            self._jr_nz,
            self._ld_hl_nn,
            self._ld_m_nn_hl,
            self._inc_hl,
            self._inc_h,
            self._dec_h,
            self._ld_h_n,
            self._daa,
            self._jr_z,
            self._add_hl_hl,
            self._ld_hl_m_nn,
            self._dec_hl,
            self._inc_l,
            self._dec_l,
            self._ld_l_n,
            self._cpl,
            self._jr_nc,
            self._ld_sp_nn,
            self._ld_m_nn_a,
            self._inc_sp,
            self._inc_m_hl,
            self._dec_m_hl,
            self._ld_m_hl_n,
            self._scf,
            self._jr_c,
            self._add_hl_sp,
            self._ld_a_m_nn,
            self._dec_sp,
            self._inc_a,
            self._dec_a,
            self._ld_a_n,
            self._ccf,
            self._ld_b_b,
            self._ld_b_c,
            self._ld_b_d,
            self._ld_b_e,
            self._ld_b_h,
            self._ld_b_l,
            self._ld_b_m_hl,
            self._ld_b_a,
            self._ld_c_b,
            self._ld_c_c,
            self._ld_c_d,
            self._ld_c_e,
            self._ld_c_h,
            self._ld_c_l,
            self._ld_c_m_hl,
            self._ld_c_a,
            self._ld_d_b,
            self._ld_d_c,
            self._ld_d_d,
            self._ld_d_e,
            self._ld_d_h,
            self._ld_d_l,
            self._ld_d_m_hl,
            self._ld_d_a,
            self._ld_e_b,
            self._ld_e_c,
            self._ld_e_d,
            self._ld_e_e,
            self._ld_e_h,
            self._ld_e_l,
            self._ld_e_m_hl,
            self._ld_e_a,
            self._ld_h_b,
            self._ld_h_c,
            self._ld_h_d,
            self._ld_h_e,
            self._ld_h_h,
            self._ld_h_l,
            self._ld_h_m_hl,
            self._ld_h_a,
            self._ld_l_b,
            self._ld_l_c,
            self._ld_l_d,
            self._ld_l_e,
            self._ld_l_h,
            self._ld_l_l,
            self._ld_l_m_hl,
            self._ld_l_a,
            self._ld_m_hl_b,
            self._ld_m_hl_c,
            self._ld_m_hl_d,
            self._ld_m_hl_e,
            self._ld_m_hl_h,
            self._ld_m_hl_l,
            self._halt,
            self._ld_m_hl_a,
            self._ld_a_b,
            self._ld_a_c,
            self._ld_a_d,
            self._ld_a_e,
            self._ld_a_h,
            self._ld_a_l,
            self._ld_a_m_hl,
            self._ld_a_a,
            self._add_a_b,
            self._add_a_c,
            self._add_a_d,
            self._add_a_e,
            self._add_a_h,
            self._add_a_l,
            self._add_a_m_hl,
            self._add_a_a,
            self._adc_a_b,
            self._adc_a_c,
            self._adc_a_d,
            self._adc_a_e,
            self._adc_a_h,
            self._adc_a_l,
            self._adc_a_m_hl,
            self._adc_a_a,
            self._sub_b,
            self._sub_c,
            self._sub_d,
            self._sub_e,
            self._sub_h,
            self._sub_l,
            self._sub_m_hl,
            self._sub_a,
            self._sbc_a_b,
            self._sbc_a_c,
            self._sbc_a_d,
            self._sbc_a_e,
            self._sbc_a_h,
            self._sbc_a_l,
            self._sbc_a_m_hl,
            self._sbc_a_a,
            self._and_b,
            self._and_c,
            self._and_d,
            self._and_e,
            self._and_h,
            self._and_l,
            self._and_m_hl,
            self._and_a,
            self._xor_b,
            self._xor_c,
            self._xor_d,
            self._xor_e,
            self._xor_h,
            self._xor_l,
            self._xor_m_hl,
            self._xor_a,
            self._or_b,
            self._or_c,
            self._or_d,
            self._or_e,
            self._or_h,
            self._or_l,
            self._or_m_hl,
            self._or_a,
            self._cp_b,
            self._cp_c,
            self._cp_d,
            self._cp_e,
            self._cp_h,
            self._cp_l,
            self._cp_m_hl,
            self._cp_a,
            self._ret_nz,
            self._pop_bc,
            self._jp_nz,
            self._jp,
            self._call_nz,
            self._push_bc,
            self._add_a_n,
            self._rst_00,
            self._ret_z,
            self._ret,
            self._jp_z,
            self._cb_prefix,
            self._call_z,
            self._call,
            self._adc_a_n,
            self._rst_08,
            self._ret_nc,
            self._pop_de,
            self._jp_nc,
            self._out_m_nn_a,
            self._call_nc,
            self._push_de,
            self._sub_n,
            self._rst_10,
            self._ret_c,
            self._exx,
            self._jp_c,
            self._in_a_m_n,
            self._call_c,
            self._dd_prefix,
            self._sbc_a_n,
            self._rst_18,
            self._ret_po,
            self._pop_hl,
            self._jp_po,
            self._ex_m_sp_hl,
            self._call_po,
            self._push_hl,
            self._and_n,
            self._rst_20,
            self._ret_pe,
            self._jp_m_hl,
            self._jp_pe,
            self._ex_de_hl,
            self._call_pe,
            self._ed_prefix,
            self._xor_n,
            self._rst_28,
            self._ret_p,
            self._pop_af,
            self._jp_p,
            self._di,
            self._call_p,
            self._push_af,
            self._or_n,
            self._rst_30,
            self._ret_m,
            self._ld_sp_hl,
            self._jp_m,
            self._ei,
            self._call_m,
            self._fd_prefix,
            self._cp_n,
            self._rst_38
        ]

    # Given two unsigned 8 bit values, make a 16 bit value.
    def _mw (self, h, l) : return h << 8 | l

    # Get the next byte at pc then incrementing pc.
    def _n (self) : b = sms.readByte (self._pc); self._pc = (self._pc + 1) & 0xFFFF; return b

    # Get the next word at pc incrementing pc.
    def _nn (self) : return self._mw (self._n (), self._n ())

    # Get a displacement value (-128 to 127)
    def _displacement(self) : b = self._n (); return b if b <= 127 else (256 - b) * -1

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
    def _ld_a_i (self) : self._a = self._i;
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

    def _jp (self) : self._pc = self._nn ()
    def _jp_c (self) : pass
    def _jp_nc (self) : pass
    def _jp_z (self) : pass
    def _jp_nz (self) : pass
    def _jp_m (self) : pass
    def _jp_p (self) : pass
    def _jp_pe (self) : pass
    def _jp_po (self) : pass
    def _jp_m_hl (self) : pass
    def _jp_m_ix (self) : pass
    def _jp_m_iy (self) : pass
    def _jr (self) : d = self._displacement (); self._pc = (self._pc + d) & 0xFFFF
    def _jr_c (self) : pass
    def _jr_nc (self) : pass
    def _jr_z (self) : pass
    def _jr_nz (self) : pass

    def _djnz (self) :
        d = self._displacement ()
        self._b = (self._b - 1) & 0xFF
        if self._b != 0 :
            self._pc = (self._pc + d) & 0xFFFF

    def _call (self) : pass
    def _call_c (self) : pass
    def _call_nc (self) : pass
    def _call_z (self) : pass
    def _call_nz (self) : pass
    def _call_m (self) : pass
    def _call_p (self) : pass
    def _call_pe (self) : pass
    def _call_po (self) : pass

    def _ret (self) : pass
    def _ret_z (self) : pass
    def _ret_nz (self) : pass
    def _ret_c (self) : pass
    def _ret_nc (self) : pass
    def _ret_m (self) : pass
    def _ret_p (self) : pass
    def _ret_pe (self) : pass
    def _ret_po (self) : pass

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
    def _inc_bc (self) : self._c = (self._c + 1) & 0xFF; if self._c == 0 : self._b = (self._b + 1) & 0xFF
    def _inc_de (self) : self._e = (self._e + 1) & 0xFF; if self._e == 0 : self._d = (self._d + 1) & 0xFF
    def _inc_hl (self) : self._l = (self._l + 1) & 0xFF; if self._l == 0 : self._h = (self._h + 1) & 0xFF
    def _inc_ix (self) : self._ixl = (self._ixl + 1) & 0xFF; if self._ixl == 0 : self._ixh = (self._ixh + 1) & 0xFF
    def _inc_iy (self) : self._iyl = (self._iyl + 1) & 0xFF; if self._iyl == 0 : self._iyh = (self._iyh + 1) & 0xFF
    def _inc_sp (self) : self._sp = (self._sp + 1) & 0xFFFF

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
    def _dec_bc (self) : self._c = (self._c - 1) & 0xFF; if self._c == 0xFF : self._b = (self._b - 1) & 0xFF
    def _dec_de (self) : self._e = (self._e - 1) & 0xFF; if self._e == 0xFF : self._d = (self._d - 1) & 0xFF
    def _dec_hl (self) : self._l = (self._l - 1) & 0xFF; if self._l == 0xFF : self._h = (self._h - 1) & 0xFF
    def _dec_ix (self) : self._ixl = (self._ixl - 1) & 0xFF; if self._ixl == 0xFF : self._ixh = (self._ixh - 1) & 0xFF
    def _dec_iy (self) : self._iyl = (self._iyl - 1) & 0xFF; if self._iyl == 0xFF : self._iyh = (self._iyh - 1) & 0xFF
    def _dec_sp (self) : self._sp = (self._sp - 1) & 0xFFFF

    def _add_a_a (self) : pass
    def _add_a_b (self) : pass
    def _add_a_c (self) : pass
    def _add_a_d (self) : pass
    def _add_a_e (self) : pass
    def _add_a_h (self) : pass
    def _add_a_l (self) : pass
    def _add_a_ixh (self) : pass
    def _add_a_ixl (self) : pass
    def _add_a_iyh (self) : pass
    def _add_a_iyl (self) : pass
    def _add_a_m_hl (self) : pass
    def _add_a_m_ixn (self) : pass
    def _add_a_m_iyn (self) : pass
    def _add_a_n (self) : pass
    def _add_hl_bc (self) : pass
    def _add_hl_de (self) : pass
    def _add_hl_hl (self) : pass
    def _add_hl_sp (self) : pass
    def _add_ix_bc (self) : pass
    def _add_ix_de (self) : pass
    def _add_ix_ix (self) : pass
    def _add_ix_sp (self) : pass
    def _add_iy_bc (self) : pass
    def _add_iy_de (self) : pass
    def _add_iy_iy (self) : pass
    def _add_iy_sp (self) : pass

    def _sub_a (self) : pass
    def _sub_b (self) : pass
    def _sub_c (self) : pass
    def _sub_d (self) : pass
    def _sub_e (self) : pass
    def _sub_h (self) : pass
    def _sub_l (self) : pass
    def _sub_n (self) : pass
    def _sub_m_hl (self) : pass
    def _sub_m_ixn (self) : pass
    def _sub_m_iyn (self) : pass

    def _adc_a_a (self) : pass
    def _adc_a_b (self) : pass
    def _adc_a_c (self) : pass
    def _adc_a_d (self) : pass
    def _adc_a_e (self) : pass
    def _adc_a_h (self) : pass
    def _adc_a_l (self) : pass
    def _adc_a_ixh (self) : pass
    def _adc_a_ixl (self) : pass
    def _adc_a_iyh (self) : pass
    def _adc_a_iyl (self) : pass
    def _adc_a_m_hl (self) : pass
    def _adc_a_m_ixn (self) : pass
    def _adc_a_m_iyn (self) : pass
    def _adc_a_n (self) : pass
    def _adc_hl_bc (self) : pass
    def _adc_hl_de (self) : pass
    def _adc_hl_hl (self) : pass
    def _adc_hl_sp (self) : pass

    def _sbc_a_a (self) : pass
    def _sbc_a_b (self) : pass
    def _sbc_a_c (self) : pass
    def _sbc_a_d (self) : pass
    def _sbc_a_e (self) : pass
    def _sbc_a_h (self) : pass
    def _sbc_a_l (self) : pass
    def _sbc_a_ixh (self) : pass
    def _sbc_a_ixl (self) : pass
    def _sbc_a_iyh (self) : pass
    def _sbc_a_iyl (self) : pass
    def _sbc_a_m_hl (self) : pass
    def _sbc_a_m_ixn (self) : pass
    def _sbc_a_m_iyn (self) : pass
    def _sbc_a_n (self) : pass
    def _sbc_hl_bc (self) : pass
    def _sbc_hl_de (self) : pass
    def _sbc_hl_hl (self) : pass
    def _sbc_hl_sp (self) : pass

    def _cp_a (self) : pass
    def _cp_b (self) : pass
    def _cp_c (self) : pass
    def _cp_d (self) : pass
    def _cp_e (self) : pass
    def _cp_h (self) : pass
    def _cp_l (self) : pass
    def _cp_ixh (self) : pass
    def _cp_ixl (self) : pass
    def _cp_iyh (self) : pass
    def _cp_iyl (self) : pass
    def _cp_m_hl (self) : pass
    def _cp_m_ixn (self) : pass
    def _cp_m_iyn (self) : pass
    def _cp_n (self) : pass

    def _or_a (self) : pass
    def _or_b (self) : pass
    def _or_c (self) : pass
    def _or_d (self) : pass
    def _or_e (self) : pass
    def _or_h (self) : pass
    def _or_l (self) : pass
    def _or_ixh (self) : pass
    def _or_ixl (self) : pass
    def _or_iyh (self) : pass
    def _or_iyl (self) : pass
    def _or_m_hl (self) : pass
    def _or_m_ixn (self) : pass
    def _or_m_iyn (self) : pass
    def _or_n (self) : pass

    def _xor_a (self) : pass
    def _xor_b (self) : pass
    def _xor_c (self) : pass
    def _xor_d (self) : pass
    def _xor_e (self) : pass
    def _xor_h (self) : pass
    def _xor_l (self) : pass
    def _xor_ixh (self) : pass
    def _xor_ixl (self) : pass
    def _xor_iyh (self) : pass
    def _xor_iyl (self) : pass
    def _xor_m_hl (self) : pass
    def _xor_m_ixn (self) : pass
    def _xor_m_iyn (self) : pass
    def _xor_n (self) : pass

    def _and_a (self) : pass
    def _and_b (self) : pass
    def _and_c (self) : pass
    def _and_d (self) : pass
    def _and_e (self) : pass
    def _and_h (self) : pass
    def _and_l (self) : pass
    def _and_ixh (self) : pass
    def _and_ixl (self) : pass
    def _and_iyh (self) : pass
    def _and_iyl (self) : pass
    def _and_m_hl (self) : pass
    def _and_m_ixn (self) : pass
    def _and_m_iyn (self) : pass
    def _and_n (self) : pass

    def _push_af (self) : pass
    def _push_bc (self) : pass
    def _push_de (self) : pass
    def _push_hl (self) : pass
    def _push_ix (self) : pass
    def _push_iy (self) : pass

    def _pop_af (self) : pass
    def _pop_bc (self) : pass
    def _pop_de (self) : pass
    def _pop_hl (self) : pass
    def _pop_ix (self) : pass
    def _pop_iy (self) : pass

    def _in_a_m_n (self) : pass

    def _rst_00 (self) : pass
    def _rst_08 (self) : pass
    def _rst_10 (self) : pass
    def _rst_18 (self) : pass
    def _rst_20 (self) : pass
    def _rst_28 (self) : pass
    def _rst_30 (self) : pass
    def _rst_38 (self) : pass

    def _rlca (self) : pass
    def _rrca (self) : pass
    def _rla (self) : pass
    def _rra (self) : pass
    def _daa (self) : pass
    def _cpl (self) : pass
    def _scf (self) : pass
    def _ccf (self) : pass

    def _out_m_nn_a (self) : pass

    def _di (self) : pass
    def _ei (self) : pass

    def _nop (self) : pass
    def _halt (self) : pass

    def _ex_af_af (self) : self._a, self._sa = self._sa, self._a; self._f, self._sf = self._sf, self._f
    def _ex_de_hl (self) : self._d, self._h = self._h, self._d; self._e, self._l = self._l, self._e
    def _exx (self) : pass
    def _ex_m_sp_hl (self) : pass

    def _cb_prefix (self) : pass
    def _dd_prefix (self) : pass
    def _ed_prefix (self) : pass
    def _fd_prefix (self) : pass

    # Returns the number of clock cycles.
    def run(self) :
        opcode = self._n ()
        self._rc = (self._rc + 1) & 0xFF
        self._opcodes[opcode]()
