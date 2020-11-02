
import decode
import getopt
import sms
import sys

_queue = [ 0x00, 0x38, 0x66 ]
_labels = []
_instructions = {}

if __name__ == '__main__' :

    opt, args = getopt.getopt (sys.argv[1:], '')
    if len (args) == 0 :
        print 'Usage: disassembler.py rom'
        exit (1)

    sms.loadRom (sys.argv[1])

    while len (_queue) > 0 :

        pc = _queue[0]
        del _queue[0]

        _labels.append (pc)

        while pc < len (sms.rom) :

            decoded = decode.decode (pc)

            if pc not in _instructions :
                _instructions[pc] = decoded

            #print '{0:04X} \t{1:06X} {2}'.format (pc, (decoded['prefix'] << 8) | decoded['opcode'], decoded['mnemonic'])
            pc += decoded['bytes']

            if decoded['prefix'] == 0x00 :

                # JMP
                if decoded['opcode'] == 0xC3 :
                    if decoded['immediate'] not in _queue and decoded['immediate'] not in _labels :
                        _queue.append (decoded['immediate'])
                        break

                # CALL
                if decoded['opcode'] == 0xCD :
                    if decoded['immediate'] not in _queue and decoded['immediate'] not in _labels :
                        _queue.append (decoded['immediate'])

                # RETN
                if decoded['opcode'] == 0xC9 :
                    break

            if decoded['prefix'] == 0xED :

                # RETN, RETI
                if decoded['opcode'] in (0x45, 0x4D) :
                    break

    _labels = sorted (_labels)

    for pc in sorted (_instructions) :

        if len (_labels) > 0 :
            if pc >= _labels[0] :

                if pc != 0 :
                    print

                print '_LABEL_{0:X}:'.format (_labels[0])
                del _labels[0]

        decoded = _instructions[pc]
        print '\t{0}'.format (decoded['mnemonic'])
        #print '{0:04X} \t{1:06X} {2}'.format (pc, (decoded['prefix'] << 8) | decoded['opcode'], decoded['mnemonic'])
