

class VDP:

    def __init__(self):
        self.first_byte_written = False
        self.display_mode = 0

        self.addr_reg = 0
        self.code_reg = 0
        self.status_reg = 0

        self.cram = bytearray(32)
        self.vram = bytearray(0x4000)
        self.read_buffer = None

    def controlPortWrite(self, byte):
        if self.first_byte_written:
            self.code_reg = byte & 0xC0
            self.addr_reg = (self.addr_reg & 0xFF) | (byte & 0x3F) << 8

            if self.code_reg == 0:
                # A byte of VRAM is read from the location defined by the
                # address register and is stored in the read buffer. The
                # address register is incremented by one. Writes to the
                # data port go to VRAM.
                self.read_buffer = self.vram[self.addr_reg]
                self.addr_reg += 1
            elif self.code_reg == 1:
                # Writes to the data port go to VRAM.
                pass
            elif self.code_reg == 2:
                # This value signifies a VDP register write, explained
                # below. Writes to the data port go to VRAM.
                pass
            elif self.code_reg == 3:
                # Writes to the data port go to CRAM.
                pass

        else:
            self.code_reg = 0
            self.addr_reg = byte & 0xFF

    def controlPortRead(self):
        self.first_byte_written = False
        return self.status_reg

    def dataPortRead(self):
        self.first_byte_written = False

    def dataPortWrite(self):
        self.first_byte_written = False
