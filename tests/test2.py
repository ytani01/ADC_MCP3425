#!/usr/bin/env python3
#
"""
 for MCP3425

   10K   10K  10K
  -^^^-+-^^^--^^^-
 |     |          |
 GND  VIN+       Vsrc

"""
import time
import threading
import pigpio
from adc_mcp3425 import MCP3425, get_logger


class Sensor(threading.Thread):
    """ Sensor """

    DEF_INTERVAL_SEC = 0.2  # sec
    DEF_AVE_N = 10

    STAT = {'NORM': 0, 'HIGH': 1, 'LOW': -1}

    __log = get_logger(__name__, False)

    def __init__(self, sensor_obj,
                 val_multiple=1, val_offset=0.0,
                 threshold_high=None, threshold_low=None,
                 interval_sec=DEF_INTERVAL_SEC,
                 ave_n=DEF_AVE_N, debug=False):
        """ init """
        self._dbg = debug
        __class__.__log = get_logger(__class__.__name__, self._dbg)
        self.__log.debug('sensor_obj=%s, interval_sec=%s',
                         sensor_obj, interval_sec)

        self._sensor = sensor_obj
        self._val_mutiple = val_multiple
        self._val_offset = val_offset
        self._threshold_high = threshold_high
        self._threshold_low = threshold_low
        self._interval_sec = interval_sec
        self._ave_n = ave_n

        self._active = False
        self._val = []
        self._cur_value = None
        self._stat = self.STAT['NORM']
        self._prev_stat = self._stat

        super().__init__(daemon=True)

    def end(self):
        """ end """
        self.__log.debug('')
        self._active = False
        self.join()
        self.__log.debug('done')

    def is_active(self):
        """ is_active """
        return self._active

    def get(self):
        """ get """
        self.__log.debug('')
        return self._cur_value

    def run(self):
        """ run """
        self.__log.debug('')

        self._active = True
        while self._active:
            value = self._sensor.get()
            value *= self._val_mutiple
            value += self._val_offset

            self._val.append(value)
            if len(self._val) > self._ave_n:
                self._val.pop(0)

            self._cur_value = sum(self._val) / len(self._val)
            self.__log.debug('cur_value=%.2f', self._cur_value)

            time.sleep(self._interval_sec)


def main():
    """ main """
    pi = pigpio.pi()

    __log = get_logger(__name__, True)

    adc = MCP3425(pi)
    sensor_th = Sensor(adc, 3, debug=True)
    sensor_th.start()
    time.sleep(1)

    try:
        while True:
            value = sensor_th.get()
            tm = time.localtime()
            print('%04d/%02d/%02d %02d:%02d:%02d, %.2f' % (
                tm.tm_year, tm.tm_mon, tm.tm_mday,
                tm.tm_hour, tm.tm_min, tm.tm_sec,
                value), flush=True)

            time.sleep(10)

    finally:
        sensor_th.end()


if __name__ == '__main__':
    main()
