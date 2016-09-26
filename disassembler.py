
import decode
import getopt
import sms
import sys

class Label(object) :

    def __init__(self) :
        self._instructions = []


_queue = [ 0x00, 0x38, 0x66 ]
_labels = {}

if __name__ == '__main__' :

    opt, args = getopt.getopt (sys.argv[1:], '')
    if len (args) == 0 :
        print 'Usage: disassembler.py rom'
        exit (1)

    sms.loadRom (sys.argv[1])

    while len (_queue) > 0 :

        pc = _queue[0]
        del _queue[0]

        label = Label ()
        _labels[pc] = label

        #print '{0:X}'.format (pc)

        while pc < len (sms.rom) :

            decoded = decode.decode (pc)
            label._instructions.append (decoded)
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


    for l in sorted (_labels) :

        print '_LABEL_{0:X}:'.format (l)

        pc = l

        for decoded in _labels[l]._instructions :
            print '{0:04X} \t{1:06X} {2}'.format (pc, (decoded['prefix'] << 8) | decoded['opcode'], decoded['mnemonic'])
            #print '\t{0}'.format (decoded['mnemonic'])
            pc += decoded['bytes']
