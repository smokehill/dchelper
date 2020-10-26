import os
import sys
import subprocess
import json
import time

from cache import Cache


class Project:

    file_path = ''
    json_data = [] # data from config.json
    cache = None

    def __init__(self):
        self.file_path = os.path.dirname(__file__) + '/config.json'
        if os.path.isfile(self.file_path) == False and os.access(self.file_path, os.R_OK) == False:
            print('{0}: {1}'.format('Error', 'Check if config.json exists and it\'s readable.'))
            sys.exit(1)

        with open(self.file_path) as f:
            self.json_data = json.load(f)

        # init cache
        self.cache = Cache()

    def stat(self):
        proc_list = self.cache.proc_list

        total = '\033[94mtotal:\033[0m \033[93m' + str(len(self.json_data)) + '\033[0m' + '\033[94m,\033[0m' 
        down = '\033[94mdown:\033[0m \033[91m' + str(len(self.json_data) - len(proc_list)) + '\033[0m' + '\033[94m,\033[0m' 
        up = '\033[94mup:\033[0m \033[92m' + str(len(proc_list)) + '\033[0m'

        print('{0} {1} {2}'.format(total, down, up))

    def list(self):
        proc_list = self.cache.proc_list

        i = 1
        for data in self.json_data:
            status = '\033[91m[-]\033[0m'
            if str(i) in proc_list:
                status = '\033[92m[+]\033[0m'

            number = '\033[93m' + str(i) + '\033[0m'
            if len(self.json_data) < 100 and i < 10:
                number = ' \033[93m' + str(i) + '\033[0m'

            print('{0} {1} {2}'.format(status, number, data['title']))
            i = i + 1

    def live(self):
        # hide cursor
        subprocess.call('tput civis', shell=True)
        subprocess.call('clear', shell=True)
 
        while True:
            self.cache = Cache()
            self.list()

            time.sleep(1)
            subprocess.call('clear', shell=True)

    def up(self):
        proc_list = self.cache.proc_list
        
        print('Project number:')
        number = raw_input('{0} '.format('>>>'))

        if number in proc_list:
            print('{0}: {1}'.format('Warning', 'Project is running.'))
            sys.exit(1)

        path = self.json_data[int(number) - 1]['path']
        status = subprocess.call('cd {0} && docker-compose up -d'.format(path), shell=True)

        if status == 0:
            self.cache.remember(number)

    def down(self):
        proc_list = self.cache.proc_list

        print('Project number:')
        number = raw_input('{0} '.format('>>>'))

        if number not in proc_list:
            print('{0}: {1}'.format('Warning', 'Project is not running.'))
            sys.exit(1)

        path = self.json_data[int(number) - 1]['path']
        status = subprocess.call('cd {0} && docker-compose down'.format(path), shell=True)

        if status == 0:
            self.cache.forget(number)

    def reset(self):
        subprocess.call('docker rm -vf $(docker ps -a -q)', shell=True)
        self.cache.forget()