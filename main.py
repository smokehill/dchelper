#!/usr/bin/python

import os
import sys
import signal
import argparse
import json

import functions as exc

parser = argparse.ArgumentParser(
    prog='tool',
    formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=30),
    description='helping tool for docker-compose projects'
)
parser.add_argument('--list', help="display docker-compose projects", action="store_true")
parser.add_argument('--up', help="docker-compose up", action="store_true")
parser.add_argument('--down', help="docker-compose down", action="store_true")
parser.add_argument('--reset', help="docker-compose down", action="store_true")
args = parser.parse_args()

# traceback Ctrl-C
signal.signal(signal.SIGINT, lambda x,y: sys.exit('\n{0}: {1}'.format('Warning', 'Abnormal termination.')))

# read json data
projects_file = os.getcwd() + '/projects.json'
if os.path.isfile(projects_file) == False and os.access(projects_file, os.R_OK) == False:
    sys.exit('{0}: {1}'.format('Error', 'Check if projects.json exists and it\'s readable.'))

with open(projects_file) as f:
    json_data = json.load(f)

def main():
    """
    Main program.
    Parses command line and executes available options.
    """

    if args.list:
        exc.list_projects(json_data)

    elif args.up:
        exc.dc_up(json_data)

    elif args.down:
        exc.dc_down(json_data)

    elif args.reset:
        exc.dc_reset()

    else:
        print("use [-h] for help")


if __name__ == '__main__':
    main()