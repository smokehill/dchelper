import os
import sys
import subprocess
import json
import time
import functools

from cache import Cache


class DCHelp:

    data = []
    cache = None

    def __init__(self):
        f_path = os.path.expanduser('~') + '/.config/dchelp/data.json'
        if os.path.isfile(f_path) == False and os.access(f_path, os.R_OK) == False:
            print('{0}: {1}'.format('Error', 'Check if ' + f_path + ' exists and it\'s readable.'))
            sys.exit(1)

        with open(f_path) as f:
            self.data = json.load(f)

        # init cache
        self.cache = Cache()

    def check_data(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            if len(self.data) == 0:
                print('{0}: {1}'.format('Info', 'No data.'))
            else:
                return func(self, *args, **kwargs)

        return wrap

    def stat(self):
        proc_list = self.cache.proc_list

        total = '\033[94mtotal:\033[0m \033[93m' + str(len(self.data)) + '\033[0m' + '\033[94m,\033[0m' 
        down = '\033[94mdown:\033[0m \033[91m' + str(len(self.data) - len(proc_list)) + '\033[0m' + '\033[94m,\033[0m' 
        up = '\033[94mup:\033[0m \033[92m' + str(len(proc_list)) + '\033[0m'

        print('{0} {1} {2}'.format(total, down, up))

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

            print('{0} {1} {2}'.format(status, number, item['title']))
            i = i + 1

    @check_data
    def live(self):
        # hide cursor
        subprocess.call('tput civis', shell=True)
        subprocess.call('clear', shell=True)
 
        while True:
            self.cache = Cache()
            self.list()

            time.sleep(1)
            subprocess.call('clear', shell=True)

    @check_data
    def up(self):
        proc_list = self.cache.proc_list
        
        print('Project number:')
        number = raw_input('{0} '.format('>>>'))

        if number in proc_list:
            print('{0}: {1}'.format('Warning', 'Project is running.'))
            sys.exit(1)

        path = self.data[int(number) - 1]['path']
        status = subprocess.call('cd {0} && docker-compose up -d'.format(path), shell=True)

        if status == 0:
            self.cache.remember(number)

    @check_data
    def down(self):
        proc_list = self.cache.proc_list

        print('Project number:')
        number = raw_input('{0} '.format('>>>'))

        if number not in proc_list:
            print('{0}: {1}'.format('Warning', 'Project is not running.'))
            sys.exit(1)

        path = self.data[int(number) - 1]['path']
        status = subprocess.call('cd {0} && docker-compose down'.format(path), shell=True)

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