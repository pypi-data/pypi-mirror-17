#!/usr/bin/env python
"""Simple CLI beep tool"""
import sys
import time
import datetime

EXIT_MSG = """Invalid arguments: {}\n---------
$ ding at hh[:mm[:ss]]
$ ding in (\digit+[smh] )+

Examples:
    $ ding at 15:30
    $ ding in 5m 30s
"""

VERSION = '0.0.1'
N_BEEPS = 4
WAIT_BEEPS = 0.15


class InvalidArguments(Exception):
    pass


def check_input(args):
    """Validate user input"""
    if len(args) < 2 or args[0] not in ['in', 'at']:
        raise InvalidArguments('insufficient number of arguments')

    if args[0] == 'in':
        if not all(arg.endswith(('s', 'm', 'h')) for arg in args[1:]):
            raise InvalidArguments('please use s/m/h suffixes')
        if not all(arg[:-1].isdigit() for arg in args[1:]):
            raise InvalidArguments('please use numbers for specifying the duration of time units')

    if args[0] == 'at':
        if len(args) > 2:
            raise InvalidArguments('too many arguments')
        if not all(arg.isnumeric() for arg in args[1].split(':')):
            raise InvalidArguments('there should only be numbers optionally separated by ":"')
        # Valid time
        try:
            datetime.time(*map(int, args[1].split(':')))
        except ValueError as e:
            raise InvalidArguments(e)

    return args

class TimeParser():
    """Class helping with parsing user provided time into seconds"""
    time_map = {
        's': 1,
        'm': 60,
        'h': 60 * 60,
    }

    def __init__(self, time, relative):
        self.time = time
        self.relative = relative

    def get_seconds(self):
        return self._get_seconds_relative() if self.relative else self._get_seconds_absolute()

    def _get_seconds_relative(self):
        return sum([self.time_map[t[-1]] * int(t[:-1]) for t in self.time])

    def _get_seconds_absolute(self):
        user_time = (datetime.datetime.combine(datetime.date.today(),
                                               datetime.time(*map(int, self.time[0].split(':')))))
        now = datetime.datetime.now()
        return ((user_time - now).seconds if user_time > now
                else (user_time + datetime.timedelta(days=1) - now).seconds)


def beep(seconds):
    """Wait `seconds` and then beep"""
    time.sleep(seconds)
    for _ in range(N_BEEPS):
        sys.stdout.write('\a')
        sys.stdout.flush()
        time.sleep(WAIT_BEEPS)


def parse_time(args):
    """Figure out the number of seconds to wait"""
    relative = True if args[0] == 'in' else False
    user_time = args[1:]
    parser = TimeParser(user_time, relative)
    return parser.get_seconds()


def main(args=sys.argv[1:]):
    if args and args[0] == '--version':
        print(VERSION)
        sys.exit()
    try:
        seconds = parse_time(check_input(args))
    except InvalidArguments as e:
        sys.exit(EXIT_MSG.format(e))
    beep(seconds)

if __name__ == '__main__':
    main()
