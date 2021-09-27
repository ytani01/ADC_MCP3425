#
# Copyright (c) 2021 Yoichi Tanibayashi
#
import time
import pigpio
import click
from . import MCP3425, SensorWatcher
from . import __prog_name__, __version__, __author__
from .my_logger import get_logger


@click.group(invoke_without_command=True,
             context_settings=dict(help_option_names=['-h', '--help']),
             help=" by " + __author__)
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, debug):
    """ command group """
    __log = get_logger(__name__, debug)

    ctx.obj = {'debug': debug}

    subcmd = ctx.invoked_subcommand
    __log.debug('subcmd=%s', subcmd)

    if not subcmd:
        print(ctx.get_help())


@cli.command(help="get")
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.option('--bus', '-b', 'bus', type=int, default=MCP3425.DEF_BUS,
              help='I2C bus: default=%s' % MCP3425.DEF_BUS)
@click.option('--addr', '-a', 'addr', type=int, default=MCP3425.DEF_ADDR,
              help='I2C address: default=0x%02X' % MCP3425.DEF_ADDR)
@click.option('--config', '-c', 'config', type=int, default=MCP3425.DEF_CONFIG,
              help='configuration bits: default=%s' % bin(MCP3425.DEF_CONFIG))
@click.option('--loop', '-l', 'loop', is_flag=True, default=False,
              help='loop option')
@click.option('--interval_sec', '-s', 'interval_sec', type=float, default=1.0,
              help='loop interval [sec]: default=1.0')
@click.option('--multiple', '-m', 'multiple', type=int, default=3,
              help='multiple: default=3')
@click.pass_obj
def get(obj, bus, addr, config, loop, interval_sec, multiple, debug):
    """ get """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s', obj)

    pi = pigpio.pi()
    adc = MCP3425(pi, bus, addr, config)

    while True:
        tm = time.localtime()
        volts = adc.get()

        print('%04d/%02d/%02d %02d:%02d:%02d, %.3f'
              % (tm.tm_year, tm.tm_mon, tm.tm_mday,
                 tm.tm_hour, tm.tm_min, tm.tm_sec,
                 volts * multiple),
              flush=True)

        if not loop:
            break
        time.sleep(interval_sec)


@cli.command(help="watch")
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.option('--bus', '-b', 'bus', type=int, default=MCP3425.DEF_BUS,
              help='I2C bus: default=%s' % MCP3425.DEF_BUS)
@click.option('--addr', '-a', 'addr', type=int, default=MCP3425.DEF_ADDR,
              help='I2C address: default=0x%02X' % MCP3425.DEF_ADDR)
@click.option('--config', '-c', 'config', type=int, default=MCP3425.DEF_CONFIG,
              help='configuration bits: default=%s' % bin(MCP3425.DEF_CONFIG))
@click.option('--interval_sec', '-s', 'interval_sec', type=float, default=2.0,
              help='loop interval [sec]: default=2.0')
@click.option('--multiple', '-m', 'multiple', type=int, default=3,
              help='multiple: default=3')
@click.pass_obj
def watch(obj, bus, addr, config, interval_sec, multiple, debug):
    """ watch """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s', obj)

    pi = pigpio.pi()
    adc = MCP3425(pi, bus, addr, config)
    sensor = SensorWatcher(adc, multiple, debug=obj['debug'] or debug)
    sensor.start()
    time.sleep(1)

    try:
        while True:
            value = sensor.get()
            tm = time.localtime()

            print('%04d/%02d/%02d %02d:%02d:%02d, %.2f'
                  % (tm.tm_year, tm.tm_mon, tm.tm_mday,
                     tm.tm_hour, tm.tm_min, tm.tm_sec,
                     value),
                  flush=True)

            time.sleep(interval_sec)

    finally:
        sensor.end()


# cli.add_command(cmd2)
# cli.add_command(cmd3)

if __name__ == '__main__':
    cli(prog_name=__prog_name__)
