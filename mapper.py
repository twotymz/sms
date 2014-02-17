
PAGE_SIZE = 0x4000

class Mapper :

    def __init__ (self) :

        self.rom = None
        self.mem = None
        self.ram = None
        self.npages = 0
        self.rampage = 0

    def read (self, addr) :
        return self.mem[addr]

    def readWord (self, addr) :
        return self.mem[addr+1] << 8 | self.mem[addr]

    def write (self, addr, value) :

        ##
        # If bit 3 is set then we are using cartridge RAM for frame 2.
        # If using cartridge RAM and bit 2 is set then we are using
        # cartridge RAM page 1 in frame 2 otherwise cartridge RAM page 0 in
        # frame 2.
        if addr == 0xFFFC :
            pass

        ##
        # Value is the page to go into frame 0. Only the last 15k of
        # the selected page though, the first kilobyte is always ROM
        # page 0.
        elif addr == 0xFFFD :
            pass

        ##
        # Value is the page to go into Frame 2. If the ram page is 0 then
        # map in the requested ROM page else map in the current RAM page.
        elif addr == 0xFFFE :
            pass
        
        else :
            self.mem[addr] = value

    def writeWord (self, addr, value) :
        self.write (addr, value & 0xFF)
        self.write (addr, value >> 8)
