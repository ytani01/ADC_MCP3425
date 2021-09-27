#
# Copywrite (c) 2021 Yoichi Tanibayashi
#
import time
import pigpio


def sign16(raw_val):
    """ sign16 """
    return (-(raw_val & 0b1000000000000000) |
             (raw_val & 0b0111111111111111))


class MCP3425:
    """ MCP3425 """

    DEF_BUS = 1
    DEF_ADDR = 0x68
    DEF_CONFIG = 0b10011000

    VREF = 2.048
    RANGE = 0b0111111111111111

    def __init__(self, pi, bus=DEF_BUS, addr=DEF_ADDR, config=DEF_CONFIG):
        """ init """

        self._pi = pi
        self._bus = bus
        self._addr = addr
        self._config = config

        self._hdr = self._pi.i2c_open(self._bus, self._addr)
        self._pi.i2c_write_byte(self._hdr, self._config)

    def get1(self):
        """ get """

        val_n, val = self._pi.i2c_read_device(self._hdr, 2)
        raw = val[0] << 8 | val[1]
        raw_s = sign16(raw)
        volts = raw_s * self.VREF / self.RANGE
        return volts

    def get(self, n=1, interval_sec=0.1):
        """ get """
        sum = self.get1()
        for i in range(n-1):
            time.sleep(interval_sec)
            sum += self.get1()

        return sum / n
