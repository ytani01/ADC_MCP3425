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
import pigpio
from MCP3425 import MCP3425


def main():
    pi = pigpio.pi()

    adc = MCP3425(pi)

    volts = []

    while True:
        v = adc.get(1, 0.01)
        #print('v=%.3f, v*3=%.3f' % (v, v*3))
        volts.append(v)
        if len(volts) > 5:
            volts.pop(0)
        tm = time.localtime()
        v_ave = sum(volts) / len(volts)
        #print('v_ave=%.3f, v_ave*3=%.3f' % (v_ave, v_ave*3))
        print('%04d/%02d/%02d %02d:%02d:%02d, %.3f' % (
            tm.tm_year, tm.tm_mon, tm.tm_mday,
            tm.tm_hour, tm.tm_min, tm.tm_sec,
            v_ave*3), flush=True)

        time.sleep(5)


if __name__ == '__main__':
    main()
