
import os
import numpy

rom = None
header = {}

# Read the ROM header and save it somewhere useful.
def readHeader () :

    global header

    header['raw'] = ''.join (['{0:02X} '.format (r) for r in rom[0x7FF0:0x8000]])
    header['tmr_sega'] = ''.join ([chr (r) for r in rom[0x7FF0:0x7FF8]])
    header['checksum'] = rom[0x7FFA] | rom[0x7FFB] << 8
    header['product_code'] = rom[0x7FFC] | rom[0x7FFD] << 8 | ((rom[0x7FFE] & 0xF0) >> 4) << 16
    header['version'] = rom[0x7FFE] & 0xF
    header['region'] = (rom[0x7FFF] & 0xF0) >> 4
    header['size'] = rom[0x7FFF] & 0xF


def readByte(pc) :
    global rom
    return rom[pc]

def readWord(pc) :
    return rom[pc] | rom[pc + 1] << 8

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
        readHeader ()
        return True

    return False
