#!/usr/bin/env python3
#
#
import pigpio
import time

BUS = 1
ADDR = 0x68
CONFIG = 0b10011000
Vref = 2.048

def sign16(raw):
    return ( -(raw & 0b1000000000000000) |
             (raw & 0b0111111111111111) )

pi = pigpio.pi()

h = pi.i2c_open(BUS, ADDR)
print('h=%d' % h)

ret = pi.i2c_write_byte(h, CONFIG)
print('ret=%d' % ret)

while True:
    (val_n, val) = pi.i2c_read_device(h, 2)
    print('%d, 0x%X%X' % (val_n, val[0], val[1]))
    raw = val[0] << 8 | val[1]
    print('raw=%X' % raw)
    raw_s = sign16(raw)
    print('raw_s=%X' % raw_s)
    volts = round((raw_s * Vref / 0b0111111111111111), 4)
    print('volts=%s' % volts)
    time.sleep(1)
