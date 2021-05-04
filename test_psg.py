import unittest
from psg import PSG

class TestPSG(unittest.TestCase):

    def test_psg(self):
        psg = PSG()
        psg.write(0x80)
        self.assertEqual(psg._channels[0].tone_noise.counter, 0)
        psg.write(0x0)
        self.assertEqual(psg._channels[0].tone_noise.counter, 0)
        psg.write(0x8F)
        self.assertEqual(psg._channels[0].tone_noise.counter, 0xF)
        psg.write(0x3F)
        self.assertEqual(psg._channels[0].tone_noise.counter, 0x3FF)
