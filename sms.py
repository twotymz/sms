
import sys
import os
import getopt
import numpy

rom = None
header = {}

# Read the ROM header and save it somewhere useful.
def _read_header () :

    global rom
    global header

    header['raw'] = ''.join (['{0:02X} '.format (r) for r in rom[0x7FF0:0x8000]])
    header['tmr_sega'] = ''.join ([chr (r) for r in rom[0x7FF0:0x7FF8]])
    header['checksum'] = rom[0x7FFA] | rom[0x7FFB] << 8
    header['product_code'] = rom[0x7FFC] | rom[0x7FFD] << 8 | ((rom[0x7FFE] & 0xF0) >> 4) << 16
    header['version'] = rom[0x7FFE] & 0xF
    header['region'] = (rom[0x7FFF] & 0xF0) >> 4
    header['size'] = rom[0x7FFF] & 0xF


# Load the rom at 'path' in to memory. Returns success.
def loadRom (path) :

    global rom
    rom = None

    file_size = os.path.getsize (path)

    with open (path, 'rb') as f :

        # Some ROMs have a superflous 512 byte header that we must skip.
        if file_size % 1024 :
            f.seek (512)
            file_size -= 512

        rom = numpy.fromfile (f, dtype=numpy.uint8)
        _read_header ()
        return True

    return False


##
# Application entry point.
if __name__ == '__main__' :

    try :
        opts, args = getopt.getopt (sys.argv[1:], '')
    except :
        print 'Usage: sms.py rom'
        sys.exit (2)

    if not loadRom (args[0]) :
        exit (2)
