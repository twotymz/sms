
import decode
import getopt
import sms
import sys


labels = []


if __name__ == '__main__' :

    opt, args = getopt.getopt (sys.argv[1:], '')
    if len (args) == 0 :
        print 'Usage: disassembler.py rom'
        exit (1)

    sms.loadRom (sys.argv[1])

    pc = 0
    while pc < len (sms.rom) :

        c, prefix, opcode, displacement, immediate, mnemonic = decode.decode (pc)
        print '{0:04X} \t{1:06X} {2}'.format (pc, (prefix << 8) | opcode, mnemonic)
        pc += c

        if prefix == 0 :

            # Long jumps...
            if opcode == 0xC3 :
                if immediate not in labels :
                    labels.append (immediate)

            # Relative jumps...
            elif opcode in (0x18, 0x20, 0x28, 0x30, 0x38) :
                #_add_label (pc + displacement)
                pass

            # Calls...
            elif opcode in (0xC4, 0xCC, 0xCD, 0xD4, 0xDC, 0xE4, 0xEC, 0xF4, 0xFC) :
                #_add_label (immediate)
                pass
