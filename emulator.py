
import z80
import getopt
import sms
import sys

##
# Application entry point.
if __name__ == '__main__' :

    try :
        opts, args = getopt.getopt (sys.argv[1:], '')
    except :
        print 'Usage: emulator.py rom'
        sys.exit (2)

    if not sms.loadRom (args[0]) :
        exit (2)

    print 'Checksum: {0:4X}'.format (sms.header['checksum'])
    print 'Product Code: {0:X}'.format (sms.header['product_code'])
    print 'Version: {0:X}'.format (sms.header['version'])
    print 'Region: {0:X}'.format (sms.header['region'])
    print 'Size: {0:X}'.format (sms.header['size'])

    cpu = z80.Z80()
    while True :
        cycles = cpu.run ()
        break
