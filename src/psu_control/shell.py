import psu_control.parsers as _parsers
from .control import ( 
    TekPS252xG as _TekPS252xG,
    TekPSUSettings as _TekPSUSettings
)
from .interpreter import ( 
    AliasCmdInterpreter as _AliasCmdInterpreter,  
    HideNoneDocMix as _HideNoneDocMix
)

__ver_info = (0,1,0)
__version__ = '.'.join(map(str, __ver_info))

class TekPS252xGShell(_AliasCmdInterpreter, _HideNoneDocMix):
    prompt = '> '
    intro = '_TekPS252xG Control Shell v{}'.format(__version__)
    doc_header = 'Commands (type help/? <topic>):'
    misc_header = 'Reference/help guides (type help/? <topic>):'
    undoc_header = None

    def __init__(self, port:str, addr:int, settings:_TekPSUSettings, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.psu = _TekPS252xG(port=port,addr=addr,output_settings=settings)

    def preloop(self):
        self.intro += '\nFound unit: {}'.format(self.psu._id)

    def do_set_voltage(self, line):
        """
        sets voltage of specified channel

        usage:
            set_voltage <channel> <voltage>

        params:
            channel: PSU channel (1-3)
            voltage: chanel output voltage (0.0-21.0 on channels 1,2, 0.0-6.5V on channel 3)
        """
        args = _parsers.parse_line(line, _parsers.set_channel_parser)
        try: 
            voltage = float(args['param'])
            if args['channel'] < 3:
                upper_bound = 21.0
            else:
                upper_bound = 6.50
            if voltage < 0.0 and voltage > upper_bound:
                raise ValueError('Voltage value too large')
            self.psu.set_voltage(args['channel'],voltage)
        except ValueError:
            self.stdout.write('Unable to parse voltage value {}'.format(args['param']))

    def do_set_current(self, line):
        """
        sets current of specified channel

        usage:
            set_voltage <channel> <voltage>

        params:
            channel: PSU channel (1-3)
            voltage: chanel output voltage (0.0-21.0 on channels 1,2, 0.0-6.5V on channel 3)
        """
        args = _parsers.parse_line(line, _parsers.set_channel_parser)
        try: 
            current = float(args['param'])
            if args['channel'] < 3:
                upper_bound = 2.5
            else:
                upper_bound = 5.0
            if current < 0.0 and current > upper_bound:
                raise ValueError('Voltage value too large')
            self.psu.set_current(args['channel'],current)
        except ValueError:
            self.stdout.write('Unable to parse voltage value {}'.format(args['param']))

    def do_set_output(self,state):
        """
        set psu output for all channels

        usage: 
            set_output <state>
        
        params:
            state: 0|1|OFF|ON where 0 is OFF and 1 is ON
        """
        if state not in {'0','1','ON','OFF'}:
            self.stdout.write('Invalid state {}'.format(state))
        else:
            if state in {'0','OFF'}:
                self.psu.set_output_enable(False)
            else:
                self.psu.set_output_enable(True)
            # self.psu.set_output_enable(state)

    def do_send_cmd(self,line):
        """
        sends arbitrary command text to unit

        usage:
            send_cmd <cmd>

        params:
            cmd: full SCPI command text to send to unit
        """
        self.psu.send_cmd(line)

    def do_read_response(self,line):
        """
        reads response from unit

        usage:
            read_response
        """
        self.stdout.write(self.psu.read_response()+'\n')

    def do_quit(self, *args):
        """
        exits the shell

        usage: 
            quit
        """
        return True

    def emptyline(self,line):
        pass

    # def do_EOF(self,*args):
        # return self.do_quit()

    alias_exit = alias_q = do_quit
    alias_sv = do_set_voltage
    alias_si = do_set_current
    alias_so = do_set_output
    alias_rr = do_read_response
    alias_sc = do_send_cmd

if __name__ == "__main__":
    import sys
    try:
        port=sys.argv[1]
        addr = sys.argv[2]
        shell = TekPS252xGShell(port=port, addr=8, settings=dict())
        shell.cmdloop()
    except IndexError:
        print('Provide port the PSU is on and it\'s GPIB address as cli args')
