
class BadPort(Exception):
    def __init__(self, port):
        self.port = port


class PortMapper:

    def __init__(self, ioport):
        self._ioport = ioport

    def read(self, port):
        if port >= 0x01 and port <= 0x3F and port % 2 == 1:
            return self._ioport.control_reg
        elif port >= 0xC0 and port <= 0xFE and port % 2 == 0:
            return self._ioport.ab_reg
        elif port >= 0xC1 and port <= 0xFF and port % 2 == 0:
            return self._ioport.bmisc_reg

        raise BadPort(port)

    def write(self, port, byte):
        pass
