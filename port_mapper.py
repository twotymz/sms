""" My attempt at emulating the SMS port mapper. """


class BadPort(Exception):
    def __init__(self, port, access):
        self.port = port
        self.access = access


class PortMapper:

    def __init__(self, ioport, vdp, psg):
        self._ioport = ioport
        self._vdp = vdp
        self._psg = psg

    def read(self, port):
        if port >= 0x01 and port <= 0x3F and port % 2 == 1:
            return self._ioport.control_reg
        elif port >= 0xC0 and port <= 0xFE and port % 2 == 0:
            return self._ioport.ab_reg
        elif port >= 0xC1 and port <= 0xFF and port % 2 == 1:
            return self._ioport.bmisc_reg
        elif port == 0xBF:
            return self._vdp.status

        raise BadPort(port, 'read')

    def write(self, port, byte):

        if port in (0x7E, 0x7F):
            self._psg.write(byte)
            return
        elif port >= 0x01 and port <= 0x3F and port % 2 == 1:
            # io control port
            return
        elif port >= 0xC0 and port <= 0xFE and port % 2 == 0:
            # io ab port
            return
        elif port >= 0xC1 and port <= 0xFF and port % 2 == 1:
            # io bmisc port
            return

        raise BadPort(port, 'write')
