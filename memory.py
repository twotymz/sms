
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
        return self._ram[addr]

    def readWord(self, addr):
        """ Reads a 16-bit value from memory at "addr".

        Args:
            addr (int)

        Returns:
            int
        """
        return self._ram[addr] | self._ram[addr + 1] << 8

    def writeByte(self, addr, v):
        pass

    def writeWord(self, addr, v):
        pass
