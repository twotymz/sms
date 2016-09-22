
import decode
import getopt
import sms
import sys

STATE_FIND_MAIN = 0
STATE_PROGRAM = 1

state = STATE_FIND_MAIN

if __name__ == '__main__' :

    opt, args = getopt.getopt (sys.argv[1:], '')
    if len (args) == 0 :
        print 'Usage: disassembler.py rom'
        exit (1)

    sms.loadRom (sys.argv[1])

    # Get a list of labels by looking for calls and jmps.

    pc = 0
    while pc < len (sms.rom) :

        c, prefix, opcode, displacement, immediate, mnemonic = decode.decode (pc)
        #print '{0:04X} \t{1:06X} {2}'.format (pc, (prefix << 8) | opcode, mnemonic)
        pc += c

        if prefix == 0 :

            if opcode == 0xC3 :
                if state == STATE_FIND_MAIN :
                    print 'main is at 0x{0:04X}'.format (immediate)
                    state= STATE_PROGRAM

                elif opcode in (0xC4, 0xCC, 0xCD, 0xD4, 0xDC, 0xE4, 0xEC, 0xF4, 0xFC) :
                    pass
