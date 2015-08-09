
import sys
import os
import getopt
import numpy
import traceback

MODE_DISASSEMBLY = 0
MODE_RAW = 1

##
# Dump the rom to standard out as hex.
def _dump (row) :
    
    byes = len (rom)
    line = ''
        
    for inst in range (offset, bytes) :
        
        line += '%02X ' % rom[inst]
        stop = inst - offset == max_instructions
        
        if (inst + 1) % 8 == 0 or stop :
            print line
            line = ''
            if stop :
                break

##
# Disassemble the rom.                
def _disassemble (rom) :
    
    bytes = len (rom)
    for inst in range (offset, bytes) :
        pass

##
# Application entry point.
if __name__ == '__main__' :
    
    mode = MODE_DISASSEMBLY
    max_instructions = -1
    offset = 0
	
    try :
        opts, args = getopt.getopt (sys.argv[1:], 'o:m:r')
        for a,o in opts :
            if a == '-m':
                max_instructions = int(o) - 1
            elif a == '-r':
                mode = MODE_RAW
            elif a == '-o' :
                offset = int(o)
    except :
        print 'Usage: disassembler.py rom'
        sys.exit (2)
       
    path = args[0]

    try :
        file_size = os.path.getsize (path)
    except :
        sys.exit (2)

    with open (path, 'rb') as f :

        # Some ROMs have a superflous 512 byte header that we must skip.
        if file_size % 1024 :
            f.seek (512)
            file_size -= 512

        rom = numpy.fromfile (f, dtype=numpy.uint8)
        
        if mode == MODE_RAW :
            _dump (rom)
        else :
            _disassemble (rom)