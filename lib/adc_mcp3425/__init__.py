#
# Copyright (c) 2021 Yoichi Tanibayashi
#
__prog_name__ = 'adc_mcp3425'
__version__ = '0.0.1'
__author__ = 'Yoichi Tanibayashi'

from .mcp3425 import MCP3425
from .my_logger import get_logger

all = ['MCP3425',
       'get_logger', __prog_name__, __version__, __author__]
