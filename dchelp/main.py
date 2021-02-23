#!/usr/bin/python

import sys
import signal
import argparse
import subprocess
import unittest

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

signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))
dchelp = DCHelp()

def main():
    if args.stat:
        dchelp.stat()

    elif args.list:
        dchelp.list()

    elif args.live:
        dchelp.live()

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