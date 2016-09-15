
import decode
import getopt
import sms
import sys


class Label(object) :

    def __init__(self, name) :
        self.name = name
        self.instructions = []


labels = {
    0x00 : Label ('_START'),
    0x66 : Label ('_NMI_HANDLER'),
    0x38 : Label ('_IRQ_HANDLER')
}


def _add_label (addr) :
    global labels
    if addr not in labels :
        labels[addr] = Label ('_LABEL_{0:X}_{1}'.format (addr, len (labels)))


def _dump_label (addr, label) :

    pc = addr
    while pc < len (sms.rom) :
        c, prefix, opcode, displacement, immediate, mnemonic = decode.decode (pc)
        pc += c


if __name__ == '__main__' :

    opt, args = getopt.getopt (sys.argv[1:], '')
    if len (args) == 0 :
        print 'Usage: disassembler.py rom'
        exit (1)

    sms.loadRom (sys.argv[1])

    current_label = labels[0]
    pc = 0
    while pc < len (sms.rom) :

        c, prefix, opcode, displacement, immediate, mnemonic = decode.decode (pc)
        print '{0:04X} \t{1:06X} {2}'.format (pc, (prefix << 8) | opcode, mnemonic)
        pc += c

        if prefix == 0 :

            if opcode == 0xC3 :
                #_add_label (immediate)
                pass

            elif opcode in (0x18, 0x20, 0x28, 0x30, 0x38) :
                #_add_label (pc + displacement)
                pass

            elif opcode in (0xC4, 0xCC, 0xCD, 0xD4, 0xDC, 0xE4, 0xEC, 0xF4, 0xFC) :
                _add_label (immediate)
