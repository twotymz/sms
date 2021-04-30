
class Memory:

    def __init__(self):
        self._ram = bytearray(0xFFFF)    # 64k of memory

    def loadCart(self, cart):
        """ Load the cartridge into memory.

        Args:
            cart (Cartridge)
        """
        # Map upto the first 3 pages of the cartridge ROM into memory.
        pages = min(cart.pages, 3)
        self._ram[:0x4000 * pages] = cart.rom[:0x4000 * pages]

    def readByte(self, addr):
        """ Reads an 8-bit value from memory at "addr".

        Args:
            addr (int)

        Returns:
            int
        """
        return self._ram[addr] & 0xFF

    def readWord(self, addr):
        """ Reads a 16-bit value from memory at "addr".

        Args:
            addr (int)

        Returns:
            int
        """
        return self.readByte(addr) | (self.readByte(addr+1) << 8)

    def writeByte(self, addr, v):
        self._ram[addr] = v & 0xFF

    def writeWord(self, addr, v):
        self.writeByte(addr, v >> 8)
        self.writeByte(addr+1, v)
