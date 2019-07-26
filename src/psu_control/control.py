from prologix_usb import PrologixSerialDecive, PSU, PSUSettings

__ver_info = (0,1,0)
__version__ = '.'.join(map(str, __ver_info))

class TekPSUSettings(PSUSettings):
    # OVP:bool
    # OCP:bool
    # tracking:str/enum NONE|SERies|PARallel
    # 
    # channels:list of dict {voltage:float, current:float, enable:bool}
    pass
class KeithleyPSUSettings(PSUSettings):
    pass

class Keithley2220G1(PSU):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._channels = 2

class TekPS252xG(PSU):
    # id will be in form: TEKTRONIX,<model>,.,SCPI:<year> FW<version>
    # 'TEKTRONIX,PS2521G, ,SCPI:94.0 FW:.15'
    # regex re.compile(r'TEKTRONIX,(?P<model>.*?),.,SCPI:(?P<year>.*?)\sFW:(?P<version>.*)',re.I)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._channels = 3