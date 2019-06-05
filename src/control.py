
import atexit
from enum import Enum
from typing import Optional
from abc import ABC, abstractmethod


import serial

PORT = 'COM11'
ADDR = 8
BAUD = 9600
TIMEOUT = 1.0

class DeviceBase(ABC):
    ENCODING = 'ascii'
    EOL = '\n'
        
    @abstractmethod
    def send_cmd(self, cmd:str):
        pass

    @abstractmethod
    def read_response(self):
        pass

class PrologixSerialDecive(DeviceBase):
    def __init__(self, port:str, baud:int=BAUD, addr:int=ADDR, timeout:float=TIMEOUT,
                 buf_clear:bool=True, init_prologix:bool=False, debug:bool=False):
        self._ser = serial.Serial(port,baud,timeout=timeout)
        atexit.register(self._ser.close)
        self._addr = addr
        self._debug = debug
        if init_prologix:
            self.send_cmd('++mode 1')
            self.send_cmd('++auto 1')
            self.send_cmd('++addr {}'.format(self._addr))
            self.send_cmd('++ver')
            # resp = self._ser.readline().strip().decode(self.ENCODING)
            resp = self.read_response()
            if 'Prologix GPIB-USB Controller' not in resp:
                raise ValueError('Unable to verify interface is a Prologix GPIB-USB Controller')
        if buf_clear:
            self.clear_buffer()

    def prologix_set_mode(self,mode):
        self.send_cmd('++mode {}'.format(mode))
    
    def send_cmd(self, cmd):
        if self._debug:
            print((cmd.strip()+self.EOL).encode(self.ENCODING))
        self._ser.write((cmd.strip()+self.EOL).encode(self.ENCODING))
    
    def read_response(self):
        data = self._ser.readline().strip().decode(self.ENCODING)
        return data

    def clear_buffer(self):
        tmp = self._ser.readline()
        while tmp != b'':
            tmp = self._ser.readline()

class TekSettings(dict):
    # OVP:bool
    # OCP:bool
    # tracking:str/enum NONE|SERies|PARallel
    # 
    # channels:list of dict {voltage:float, current:float, enable:bool}
    pass

DEFAULT_SETTINGS = TekSettings()

class TekPS252xG(PrologixSerialDecive):
    def __init__(self, output_settings:TekSettings=DEFAULT_SETTINGS, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._settings = output_settings
        self._id:str = self.get_id()
        self._channels = 3

    def get_id(self):
        self.send_cmd('*idn?')
        # id will be in form: TEKTRONIX,<model>,.,SCPI:<year> FW<version>
        # 'TEKTRONIX,PS2521G, ,SCPI:94.0 FW:.15'
        # regex re.compile(r'TEKTRONIX,(?P<model>.*?),.,SCPI:(?P<year>.*?)\sFW:(?P<version>.*)',re.I)
        resp = self.read_response()
        return resp

    def self_test(self) -> Optional[bool]:
        self.send_cmd('*TST?')
        # self test takes ___ many seconds, maybe sleep
        resp = int(self.read_response())
        if resp == 0:
            return True
        elif resp == -300:
            return False
        else:
            return None

    def sel_channel(self, channel:int):
        self.send_cmd('INST:NSEL {}'.format(channel))

    def update_settings(self,settings:TekSettings):
        pass

    def set_output_enable(self,output_state:bool):
        self.send_cmd('OUTP {}'.format('ON' if output_state else 'OFF'))

    def set_voltage(self,channel:int,voltage:float):
        self.sel_channel(channel)
        self.send_cmd('SOUR:VOLT {}'.format(voltage))
    
    def set_current(self,channel:int,current:float):
        self.sel_channel(channel)
        self.send_cmd('SOUR:CURR {}'.format(current))

    def disable_all(self):
        self.set_output_enable(False)

if __name__ == "__main__":
    # psu = TekPS252xG(port=PORT)
    pass
