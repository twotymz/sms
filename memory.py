
class Memory:

    def __init__(self):
        self._ram = bytearray(0xFFFF)    # 64k of memory

    def load_cart(self, cart):
        """ Load the cartridge into memory.

        Args:
            cart (Cartridge)
        """
        # Map upto the first 3 pages of the cartridge ROM into memory.
        pages = min(cart.pages, 3)
        self._ram[:0x4000 * pages] = cart.rom[:0x4000 * pages]

    def read(self, addr):
        """ Reads an 8-bit value from memory at "addr".

        Args:
            addr (int)

        Returns:
            int
        """
        return self._ram[addr] & 0xFF

    def read_word(self, addr):
        """ Reads a 16-bit value from memory at "addr".

        Args:
            addr (int)

        Returns:
            int
        """
        return self.read(addr) | (self.read(addr+1) << 8)

    def write(self, addr, v):
        self._ram[addr] = v & 0xFF

    def write_word(self, addr, v):
        self.write(addr, v)
        self.write(addr+1, v >> 8)
