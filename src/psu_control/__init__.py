__version_info = (0,0,1)
__version__ = '.'.join(map(str,__version_info))

from .control import PSU, PSUSettings,  TekPS252xG, TekPSUSettings, Keithley2220G1, KeithleyPSUSettings
from . import shell
