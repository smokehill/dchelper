import os
import sys
import subprocess
import json
import time
import functools
import curses

from cache import Cache


class DCHelp:

    data = []
    cache = None

    def __init__(self):
        # init data
        f_path = os.path.expanduser('~') + '/.config/dchelp/data.json'
        if os.path.isfile(f_path) == False and os.access(f_path, os.R_OK) == False:
            print("%s not exists or not readable." % f_path)
            sys.exit(1)
        with open(f_path) as f:
            self.data = json.load(f)

        # init cache
        self.cache = Cache()

    def check_data(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            if len(self.data) == 0:
                print('No projects.')
            else:
                return func(self, *args, **kwargs)
        return wrap

    def stat(self):
        proc_list = self.cache.proc_list

        total = "\033[94m{title}\033[0m \033[93m{number}\033[0m\033[94m{char}\033[0m".format(title='total:', number=str(len(self.data)), char=',')
        down = "\033[94m{title}\033[0m \033[91m{number}\033[0m\033[94m{char}\033[0m".format(title='down:', number=(str(len(self.data) - len(proc_list))), char=',')
        up = "\033[94m{title}\033[0m \033[92m{number}\033[0m".format(title='up:', number=str(len(proc_list)))

        print("{total} {down} {up}".format(total=total, down=down, up=up))

    @check_data
    def list(self):
        proc_list = self.cache.proc_list

        i = 1
        for item in self.data:
            status = '\033[91m[-]\033[0m'
            if str(i) in proc_list:
                status = '\033[92m[+]\033[0m'

            number = '\033[93m' + str(i) + '\033[0m'
            if len(self.data) < 100 and i < 10:
                number = ' \033[93m' + str(i) + '\033[0m'

            print("{status} {number} {title}".format(status=status, number=number, title=item['title']))
            i = i + 1

    @check_data
    def live(self, stdscr):
        k = 0
        total_lines = curses.LINES - 1
        start = 0
        end = total_lines

        stdscr.clear()
        stdscr.refresh()

        curses.curs_set(0)
        curses.use_default_colors()

        curses.start_color()
        curses.init_pair(1, 0, 2)

        while (k != ord('q')):

            stdscr.clear()
            self.cache = Cache()

            height, width = stdscr.getmaxyx()

            if k == curses.KEY_RIGHT:
                if len(self.data) > total_lines and len(self.data[start:end]) > start:
                    start += total_lines
                    end += start

            if k == curses.KEY_LEFT:
                if start >= total_lines:
                    start -= total_lines
                    end -= start

            # projects list
            proc_list = self.cache.proc_list

            i = 0
            j = start + 1

            for item in self.data[start:end]:
                if i < total_lines:
                    status = '[+]' if str(j) in proc_list else '[-]'
                    number = ' ' + str(j) if len(self.data) < 100 and j < 10 else str(j)

                    stdscr.addstr(i, 0, "{status} {number} {title}".format(
                        status=status,
                        number=number,
                        title=item['title']
                    ))

                    i = i + 1
                    j = j + 1

            # bottom info
            bottom_info = "[<]=Prev [>]=Next [q]=Exit"
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(height - 1, 0, bottom_info)
            stdscr.addstr(height - 1, len(bottom_info), " " * (width - len(bottom_info) - 1))
            stdscr.attroff(curses.color_pair(1))

            stdscr.timeout(1000) # 1 sec.
            stdscr.refresh()

            k = stdscr.getch()


    @check_data
    def up(self):
        proc_list = self.cache.proc_list

        try:
            print('Project number:')
            number = int(raw_input('>>> '))
            if number is None or number <= 0 or number > len(self.data):
                print('Bad argument!')
                sys.exit(1)
        except ValueError:
            print('Bad argument!')
            sys.exit(1)

        if str(number) in proc_list:
            print('Project is running.')
            sys.exit(1)

        path = self.data[int(number) - 1]['path']
        status = subprocess.call("cd %s && docker-compose up -d" % path, shell=True)

        if status == 0:
            self.cache.remember(number)

    @check_data
    def down(self):
        proc_list = self.cache.proc_list

        try:
            print('Project number:')
            number = int(raw_input('>>> '))
            if number is None or number <= 0 or number > len(self.data):
                print('Bad argument!')
                sys.exit(1)
        except ValueError:
            print('Bad argument!')
            sys.exit(1)

        if str(number) not in proc_list:
            print('Project is not running.')
            sys.exit(1)

        path = self.data[int(number) - 1]['path']
        status = subprocess.call("cd %s && docker-compose down" % path, shell=True)

        if status == 0:
            self.cache.forget(number)

    def reset(self):
        print('Stopping and removing containers...')
        subprocess.call('docker stop $(docker ps -a -q)', shell=True)
        subprocess.call('docker rm $(docker ps -a -q)', shell=True)

        print('\nRemoving networks...')
        subprocess.call('docker network prune -f', shell=True)

        print('Removing volumes...')
        subprocess.call('docker volume prune -f', shell=True)

        self.cache.forget()