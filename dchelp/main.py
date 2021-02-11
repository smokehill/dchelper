#!/usr/bin/python

import sys
import signal
import argparse
import subprocess
import unittest
import curses

import tests
from dchelp import DCHelp


parser = argparse.ArgumentParser(
    prog='dchelp',
    formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=30),
    description='wrappers for docker-compose'
)
parser.add_argument('--stat', help="common statistics", action="store_true")
parser.add_argument('--list', help="projects list", action="store_true")
parser.add_argument('--live', help="projects list (live mode)", action="store_true")
parser.add_argument('--up', help="up project", action="store_true")
parser.add_argument('--down', help="down project", action="store_true")
parser.add_argument('--reset', help="down all projects", action="store_true")
parser.add_argument('--test', help="unit tests", action="store_true")
args = parser.parse_args()

# traceback Ctrl-C
def fire_escape(signum, frame):
    # show cursor
    subprocess.call('tput cnorm', shell=True)
    sys.exit(0)

signal.signal(signal.SIGINT, fire_escape)
dchelp = DCHelp()

def main():
    if args.stat:
        dchelp.stat()

    elif args.list:
        dchelp.list()

    elif args.live:
        curses.wrapper(dchelp.live)

    elif args.up:
        dchelp.up()

    elif args.down:
        dchelp.down()

    elif args.reset:
        dchelp.reset()

    elif args.test:
        suite = unittest.TestLoader().loadTestsFromModule(tests)
        unittest.TextTestRunner().run(suite)

    else:
        print("use [-h] for help")


if __name__ == '__main__':
    main()