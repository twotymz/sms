
import decode
import getopt
import sms
import sys

if __name__ == '__main__' :

    opt, args = getopt.getopt (sys.argv[1:], '')
    if len (args) == 0 :
        print 'Usage: disassembler.py rom'
        exit (1)

    if not sms.loadRom (args[0]) :
        exit (1)

    pc = 0
    while pc < len (sms.rom) :

        c, mnemonic, displacement, immediate = decode.decode (pc)
        print pc, mnemonic, displacement, immediate
        pc += c
