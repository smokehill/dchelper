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
    def live(self):
        curses.wrapper(self.init_live)

    def init_live(self, stdscr):
        colors = {
            'black': curses.COLOR_BLACK,        # 0
            'red': curses.COLOR_RED,            # 1
            'green': curses.COLOR_GREEN,        # 2
            'yellow': curses.COLOR_YELLOW,      # 3
            'blue': curses.COLOR_BLUE,          # 4
            'magenta': curses.COLOR_MAGENTA,    # 5
            'cyan': curses.COLOR_CYAN,          # 6
            'white': curses.COLOR_WHITE,        # 7
            'default': -1
        }
        k = 0
        win_height, win_width = stdscr.getmaxyx()
        dc_total = win_height - 2
        dc_start = 0
        dc_end = dc_total

        stdscr.clear()
        stdscr.refresh()

        curses.curs_set(0)
        curses.use_default_colors()

        curses.start_color()
        curses.init_pair(1, colors['black'], colors['white'])
        curses.init_pair(2, colors['white'], colors['default'])
        curses.init_pair(3, colors['green'], colors['default'])
        curses.init_pair(4, colors['red'], colors['default'])
        curses.init_pair(5, colors['yellow'], colors['default'])

        while (k != ord('q')):
            stdscr.clear()
            self.cache = Cache()
            proc_list = self.cache.proc_list
            win_height, win_width = stdscr.getmaxyx()

            if win_height < 10 or win_width < 40:
                # catch small screen
                title = 'TERMINAL TO SMALL'
                c_y, c_x = int((win_height // 2) - 1), int((win_width // 2) - (len(title) // 2) - len(title) % 2)
                stdscr.addstr(c_y, c_x, title, curses.color_pair(4))
            else:
                if k == curses.KEY_RESIZE:
                    title = 'TERMINAL RESIZE...'
                    c_y, c_x = int((win_height // 2) - 1), int((win_width // 2) - (len(title) // 2) - len(title) % 2)
                    stdscr.addstr(c_y, c_x, title, curses.color_pair(4))
                    # reset params on screen resize
                    dc_total = win_height - 2
                    dc_start = 0
                    dc_end = dc_total
                else:
                    # track arrow right
                    if k == curses.KEY_RIGHT:
                        if len(self.data) > dc_total and len(self.data[dc_start:dc_end]) > dc_start:
                            dc_start += dc_total
                            dc_end += dc_start
                    # track arrow left
                    if k == curses.KEY_LEFT:
                        if dc_start >= dc_total:
                            dc_start -= dc_total
                            dc_end -= dc_start
                    # list projects
                    i = 0
                    j = dc_start + 1
                    for item in self.data[dc_start:dc_end]:
                        if i < dc_total:
                            status = '[+]' if str(j) in proc_list else '[-]'
                            number = ' ' + str(j) if len(self.data) < 100 and j < 10 else str(j)
                            if str(j) in proc_list:
                                stdscr.addstr(i, 0, status, curses.color_pair(3))
                            else:
                                stdscr.addstr(i, 0, status, curses.color_pair(4))
                            if len(self.data) < 10:
                                stdscr.addstr(i, 3, number, curses.color_pair(5))
                                stdscr.addstr(i, 6, item['title'], curses.color_pair(2))
                            else:
                                stdscr.addstr(i, 4, number, curses.color_pair(5))
                                stdscr.addstr(i, 7, item['title'], curses.color_pair(2))
                            i = i + 1
                            j = j + 1
                    # bottom info
                    stdscr.addstr(win_height - 1, 0, ' < ', curses.color_pair(1))
                    stdscr.addstr(win_height - 1, 4, 'Prev', curses.color_pair(2))
                    stdscr.addstr(win_height - 1, 9, ' > ', curses.color_pair(1))
                    stdscr.addstr(win_height - 1, 13, 'Next', curses.color_pair(2))
                    stdscr.addstr(win_height - 1, 18, ' q ', curses.color_pair(1))
                    stdscr.addstr(win_height - 1, 22, 'Exit', curses.color_pair(2))

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