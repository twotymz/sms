

class Z80:

    def __init__(self):

        self._interrupts_enabled = True
        self._af[2] = 0
        self._bc[2] = 0
        self._de[2] = 0
        self._hl[2] = 0
        self._ix = 0
        self._iy = 0
        self._sp = 0
        self._i = 0
        self._r = 0
        self._pc = 0

        self._instructions = {
            0xF3: self._di
        }

    def run(self, byte, word):

        decoded = decode.decode(self._pc, byte, word)
        self._pc += decoded.bytes

        instruction = decoded.prefix << 8 | decoded.opcode

        try:

            d = self._instructions[instruction]
            d(self, decoded)

        except KeyError:
            print('Unhandled instruction')
            print(decoded)
            raise

    def _di(self, d):
        self._interrupts_enabled = False
