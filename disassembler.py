
import decode
import getopt
import sms
import sys

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
