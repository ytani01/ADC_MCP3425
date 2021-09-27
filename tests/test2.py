#!/usr/bin/env python3
#
# for MCP3425
#
#   10K   10K  10K
#  -^^^-+-^^^--^^^-
# |     |          |
# GND  VIN+       Vsrc
#
import time
import threading
import pigpio
from adc_mcp3425 import MCP3425, get_logger


class Sensor(threading.Thread):
    """ Sensor """

    DEF_INTERVAL_SEC = 1.0  # sec

    __log = get_logger(__name__, False)

    def __init__(self, interval_sec=DEF_INTERVAL_SEC, debug=False):
        """ init """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('interval_sec=%s', interval_sec)

        self._interval_sec = interval_sec

        self._active = False

        super().__init__(daemon=True)

    def end(self):
        """ end """
        selt._active = False



def main():
    pi = pigpio.pi()

    __log = get_logger(__name__, True)

    adc = MCP3425(pi)

    volts = []

    while True:
        v = adc.get(1, 0.01)
        volts.append(v)
        if len(volts) > 5:
            volts.pop(0)
        tm = time.localtime()
        v_ave = sum(volts) / len(volts)
        __log.debug('v_ave=%s', v_ave)
        print('%04d/%02d/%02d %02d:%02d:%02d, %.3f' % (
            tm.tm_year, tm.tm_mon, tm.tm_mday,
            tm.tm_hour, tm.tm_min, tm.tm_sec,
            v_ave*3), flush=True)

        time.sleep(5)


if __name__ == '__main__':
    main()
