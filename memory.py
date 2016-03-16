
import numpy

class Mapper(object) :

    def __init__(self) :
        self.rom = None
        self.ram = None

    def initalize (self, rom) :
        self.rom = rom
        self.ram = self.rom[0:0x8000]           # map the first 64K of the rom

    def read (self, pc) :
        return self.ram[pc]

    def readWord (self, pc) :
        return self.ram[pc] | self.ram[pc] << 8

    def write (self, addr, v) :
        pass

    def writeWord (self, addr, v) :
        pass
