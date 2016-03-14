
import sys
import os
import getopt
import numpy
import mapper
import cpu

rom = None

def readRom (path) :

    global rom
    rom = None

    try :

        file_size = os.path.getsize (path)

        with open (path, 'rb') as f :

            # Some ROMs have a superflous 512 byte header that we must skip.
            if file_size % 1024 :
                f.seek (512)
                file_size -= 512

            rom = numpy.fromfile (f, dtype=numpy.uint8)

    except :
        print str (err)


##
# Application entry point.
if __name__ == '__main__' :

    try :
        opts, args = getopt.getopt (sys.argv[1:], '')
    except :
        print str (err)
        print 'Usage: sms.py rom'
        sys.exit (2)

    cpu = cpu.CPU ()
    memory = mapper.Mapper ()

    if not _load_rom (args[0], memory) :
        sys.exit (2)

    cpu.step (memory)
    cpu.step (memory)
