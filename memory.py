
class Memory:

    def __init__(self):
        self._memory = bytearray(0xFFFF)
        print(self._memory[0])

    def loadCart(self, cart):
        self._memory[:0xC]

    def readByte(self, addr):
        return self._memory[addr]

    def readWord(self, addr):
        return self._memory[addr] | self._memory[addr + 1] << 8

    def writeByte(self, addr, v):
        pass

    def writeWord(self, addr, v):
        pass
