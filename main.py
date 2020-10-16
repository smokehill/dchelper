#!/usr/bin/python

import os
import sys
import signal
import argparse
import subprocess
# import unittest
# import tests

from project import Project


parser = argparse.ArgumentParser(
    prog='tool',
    formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=30),
    description='wrappers for docker-compose'
)
parser.add_argument('--list', help="display docker-compose projects", action="store_true")
parser.add_argument('--up', help="docker-compose up", action="store_true")
parser.add_argument('--down', help="docker-compose down", action="store_true")
parser.add_argument('--reset', help="docker-compose down for all", action="store_true")
parser.add_argument('--test', help="unit tests", action="store_true")
args = parser.parse_args()

# traceback Ctrl-C
signal.signal(signal.SIGINT, lambda x,y: sys.exit('\n{0}: {1}'.format('Warning', 'Abnormal termination.')))

project = Project()

def main():
    if args.list:
        project.list()

    elif args.up:
        project.up()

    elif args.down:
        project.down()

    elif args.reset:
        project.reset()

    elif args.test:
        run_tests = os.path.dirname(__file__) + '/tests.py'
        subprocess.call("python {0}".format(run_tests), shell=True)
        print("use [-h] for help")


if __name__ == '__main__':
    main()