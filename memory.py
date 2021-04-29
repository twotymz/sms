import numpy as np

class Memory:

    def __init__(self):
        self._memory = np.zeros(0xFFFF, dtype=np.uint8)
        print(self._memory[0])

    def loadCart(self, cart):
        np.put(self._memory, np.arange(0x3FFF), cart._rom)
        print(self._memory[0])

    def readByte(self, addr):
        return self._memory[addr]

    def readWord(self, addr):
        return self._memory[addr] | self._memory[addr + 1] << 8

    def writeByte(self, addr, v):
        pass

    def writeWord(self, addr, v):
        pass
