#!/usr/bin/python

import os
import sys
import signal
import argparse
import subprocess
import unittest

import tests
from project import Project


parser = argparse.ArgumentParser(
    prog='tool',
    formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=30),
    description='wrappers for docker-compose'
)
parser.add_argument('--list', help="projects list", action="store_true")
parser.add_argument('--live', help="projects list (live mode)", action="store_true")
parser.add_argument('--up', help="up project", action="store_true")
parser.add_argument('--down', help="down project", action="store_true")
parser.add_argument('--reset', help="down all projects", action="store_true")
parser.add_argument('--test', help="unit tests", action="store_true")
args = parser.parse_args()

def fire_escape(signum, frame):
    # show cursor
    os.system('tput cnorm')
    sys.exit('\n{0}: {1}'.format('Warning', 'Abnormal termination.'))

# traceback Ctrl-C
signal.signal(signal.SIGINT, fire_escape)

project = Project()

def main():
    if args.list:
        project.list()

    elif args.live:
        project.live()

    elif args.up:
        project.up()

    elif args.down:
        project.down()

    elif args.reset:
        project.reset()

    elif args.test:
        suite = unittest.TestLoader().loadTestsFromModule(tests)
        unittest.TextTestRunner().run(suite)

    else:
        print("use [-h] for help")


if __name__ == '__main__':
    main()