""" My attempt at emulating the IO ports of the Sega Master System.

Based on the information provided here: https://www.smspower.org/Development/PeripheralPorts#PortDCIOPortAAndB
"""

class IOPort:

    def __init__(self):
        self._control = 0            # port control bits
        self._ab = 0                 # i/o port a and b
        self._bmisc = 0              # i/o port b and misc
        self.reset()

    def reset(self):
        self._control = 0xF          # all low bits set
        self._ab = 0xFF              # all bits set (unconnected)
        self._bmisc = 0xFF           # all bits set (unconnected)

    @property
    def control_reg(self):
        return self._control

    @property
    def ab_reg(self):
        return self._ab

    @property
    def bmisc_reg(self):
        return self._bmisc

    # Reset button control methods. Set methods pull pin to ground and reset
    # sets it back to high (unconnected).

    def reset_set(self):
        self._bmisc = self._bmisc & ~0x10

    def reset_unset(self):
        self._bmisc = self._bmisc | 0x10

    # Port A control methods. Set methods pull pin to ground and reset
    # sets it back to high (unconnected).

    def port_a_up_set(self):
        self._ab = self._ab & ~0x1

    def port_a_up_reset(self):
        self._ab = self._ab | 0x1

    def port_a_down_set(self):
        self._ab = self._ab & ~0x2

    def port_a_down_reset(self):
        self._ab = self._ab | 0x2

    def port_a_left_set(self):
        self._ab = self._ab & ~0x4

    def port_a_left_reset(self):
        self._ab = self._ab | 0x4

    def port_a_right_set(self):
        self._ab = self._ab & ~0x8

    def port_a_right_reset(self):
        self._ab = self._ab | 0x8

    def port_a_tl_set(self):
        self._ab = self._ab & ~0x10

    def port_a_tl_reset(self):
        self._ab = self._ab | 0x10

    def port_a_tr_set(self):
        self._ab = self._ab & ~0x20

    def port_a_tr_reset(self):
        self._ab = self._ab | 0x20

    def port_a_th_set(self):
        self._bmisc = self._bmisc & ~0x40

    def port_a_th_reset(self):
        self._bmisc = self._bmisc | 0x40

    # Port B control methods. Set methods pull pin to ground and reset
    # sets it back to high (unconnected).

    def port_b_up_set(self):
        self._ab = self._ab & ~0x40

    def port_b_up_reset(self):
        self._ab = self._ab | 0x40

    def port_b_down_set(self):
        self._ab = self._bmisc & ~0x80

    def port_b_down_reset(self):
        self._ab = self._ab | 0x80

    def port_b_left_set(self):
        self._bmisc = self._bmisc & ~0x01

    def port_b_left_reset(self):
        self._bmisc = self._bmisc | 0x01

    def port_b_right_set(self):
        self._bmisc = self._bmisc & ~0x02

    def port_b_right_reset(self):
        self._bmisc = self._bmisc | 0x02

    def port_b_tl_set(self):
        self._bmisc = self._bmisc & ~0x04

    def port_b_tl_reset(self):
        self._bmisc = self._bmisc | 0x04

    def port_b_tr_set(self):
        self._bmisc = self._bmisc & ~0x08

    def port_b_tr_reset(self):
        self._bmisc = self._bmisc | 0x08

    def port_b_th_set(self):
        self._bmisc = self._bmisc & ~0x80

    def port_b_th_reset(self):
        self._bmisc = self._bmisc | 0x80
