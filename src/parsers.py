# vim:fileencoding=utf-8
# -*- coding: utf-8 -*-
"""
psu_control
parsers.py
Author: Danyal Ahsanullah
Copyright (c):  2017 Danyal Ahsanullah
License: N/A
Description:
    parsers and parser fetching procedures for vaildating user input to shells.
"""
import argparse 
from gettext import gettext as _
import sys as _sys


class ReadParser(argparse.ArgumentParser):
    """
    Overloaded class to disable help flags by default.
    Otherwise identical to argparse.ArgumentParser
    """
    def __init__(self, *args, **kwargs):
        super(ReadParser, self).__init__(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                         add_help=False, *args, **kwargs)

    def error(self, message):
        """
        error(message: string)
        modified to not raise SystemExit
        """
        self.print_usage(_sys.stderr)
        args = {'prog': self.prog, 'message': message}
        self._print_message(_('%(prog)s: error: %(message)s\n') % args, _sys.stderr)


def parse_line(line, parser):
    arguments = filter(None, line.split(' '))
    return unpack_ns(parser.parse_args(arguments))


def get_parser_params(parser):
    # noinspection PyProtectedMember
    return parser._option_string_actions.keys()


def unpack_ns(namespace):
    """
    convert argparse returned namespace into a dictionary for use as the **kwargs argument to a function
    """
    return vars(namespace)

# set a channel and parameter
set_channel_parser = ReadParser('set_channel_parser')
set_channel_parser.add_argument('channel', action='store', type=int, default=1, choices=range(1,3+1),
                                help='channel to set')
set_channel_parser.add_argument('param', action='store', type=str, default=1,help='parameter to set for the channel')


# # div cmd parser
# div_parser = ReadParser('voltage_divider')
# div_parser.add_argument('-i', '--vin', action='store', type=phy_val, default=None)
# div_parser.add_argument('-o', '--vout', action='store', type=phy_val, default=None)
# div_parser.add_argument('-1', '--x1', action='store', type=phy_val, default=None)
# div_parser.add_argument('-2', '--x2', action='store', type=phy_val, default=None)
# div_parser.add_argument('-e', '--e_range', action='store', type=str, default=None)

# # intrinsic_temperature_table parser
# itt_parser = ReadParser('intrinsic_temperature_table')
# itt_parser.add_argument('materials', action='store', type=str, nargs='+', default=['Si'])
# itt_parser.add_argument('--start', action='store', type=int, default=300)
# itt_parser.add_argument('--stop', action='store', type=int, default=300)
# itt_parser.add_argument('--step', action='store', type=int, default=100)


launch_parser = argparse.ArgumentParser('electronics_calc', 'set of calculators to handle assortment of tasks related'
                                                            ' to Electrical engineering applications')
launch_parser.add_argument('-M', '--mode', action='store', type=str, default=None)

if __name__ == '__main__':
    # components_parser.print_help()
    # itt_parser.print_help()
    # div_parser.print_help()
    pass