from dataclasses import dataclass


@dataclass
class Register:
    """ 16-bit register implementation. """
    lo: int = 0
    hi: int = 0

    @property
    def reg(self):
        return self.hi << 8 | self.lo

    @reg.setter
    def reg(self, v):
        self.lo = v & 0xFF
        self.hi = v >> 8

    def __repr__(self):
        return f'0x{self.reg:04X}'


@dataclass
class Z80:

    af: Register = Register()
    bc: Register = Register()
    de: Register = Register()
    hl: Register = Register()

    af_: Register = Register()
    bc_: Register = Register()
    de_: Register = Register()
    hl_: Register = Register()

    i: int = 0
    r: int = 0
    ix: Register = Register()
    iy: Register = Register()
    sp: Register = Register()
    pc: Register = Register()

    @property
    def s_flag(self):
        return (self.af.lo & 0x80) >> 7

    def s_set(self):
        self.af.lo = self.af.lo | 0x80

    def s_reset(self):
        self.af.lo = self.af.lo & ~0x80

    @property
    def z_flag(self):
        return (self.af.lo & 0x40) >> 6

    def z_set(self):
        self.af.lo = self.af.lo | 0x40

    def z_reset(self):
        self.af.lo = self.af.lo & ~0x40

    @property
    def h_flag(self):
        return (self.af.lo & 0x10) >> 4

    def h_set(self):
        self.af.lo = self.af.lo | 0x10

    def h_reset(self):
        self.af.lo = self.af.lo & ~0x10

    @property
    def pv_flag(self):
        return (self.af.lo & 0x04) >> 2

    def pv_set(self):
        self.af.lo = self.af.lo | 0x04

    def pv_reset(self):
        self.af.lo = self.af.lo & ~0x04

    @property
    def n_flag(self):
        return (self.af.lo & 0x02) >> 1

    def n_set(self):
        self.af.lo = self.af.lo | 0x02

    def n_reset(self):
        self.af.lo = self.af.lo & ~0x02

    @property
    def c_flag(self):
        return self.af.lo & 0x01

    def c_set(self):
        self.af.lo = self.af.lo | 0x01

    def c_reset(self):
        self.af.lo = self.af.lo & ~0x01

    def __repr__(self):
        s  = f" AF: {self.af} BC: {self.bc} DE: {self.de} HL: {self.hl}"
        s += f" AF': {self.af_} BC': {self.bc_} DE': {self.de_} HL': {self.hl_}\n"
        s += f" SP: {self.sp} PC: {self.pc} IX: {self.ix} IY: {self.iy} I: 0x{self.i:02X} R: 0x{self.r:02X}\n"
        s += f" S: {self.s_flag} Z: {self.z_flag} H: {self.h_flag} N: {self.n_flag} C: {self.c_flag}"
        return s
