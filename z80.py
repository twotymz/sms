from dataclasses import dataclass

@dataclass
class Register:
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

    def __repr__(self):
        s  = f" AF: {self.af} BC: {self.bc} DE: {self.de} HL: {self.hl} "
        s += f"AF': {self.af_} BC': {self.bc_} DE': {self.de_} HL': {self.hl_}\n"
        s += f" SP: {self.sp} PC: {self.pc} IX: {self.ix} IY: {self.iy} I: 0x{self.i:02X} R: 0x{self.r:02X}"
        return s
