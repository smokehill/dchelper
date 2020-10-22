import os
import sys
import subprocess
import json
import time

from cache import Cache


class Project:

    file_path = ''
    json_data = [] # data from projects.json
    cache = None

    def __init__(self):
        self.file_path = os.path.dirname(__file__) + '/projects.json'
        if os.path.isfile(self.file_path) == False and os.access(self.file_path, os.R_OK) == False:
            print('{0}: {1}'.format('Error', 'Check if projects.json exists and it\'s readable.'))
            sys.exit(1)

        with open(self.file_path) as f:
            self.json_data = json.load(f)

        # init cache
        self.cache = Cache()

    def list(self):
        proc_list = self.cache.proc_list

        i = 1
        for data in self.json_data:
            status = '\033[91m[-]\033[0m'
            if str(i) in proc_list:
                status = '\033[92m[+]\033[0m'
    
            number = '\033[33m' + str(i) + '\033[0m'
            if len(self.json_data) < 100 and i < 10:
                number = ' \033[33m' + str(i) + '\033[0m'
    
            print('{0} {1} {2}'.format(status, number, data['title']))
            i = i + 1

    def live(self):
        # hide cursor
        subprocess.call('tput civis', shell=True)
 
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

        try:
            path = self.json_data[int(number) - 1]['path']
            subprocess.call('cd {0} && docker-compose up -d'.format(path), shell=True)
            self.cache.remember(number)
        except Exception as e:
            print("{0}: {1}".format('Error', e))
            sys.exit(1)

    def down(self):
        proc_list = self.cache.proc_list

        print('Project number:')
        number = raw_input('{0} '.format('>>>'))

        if number not in proc_list:
            print('{0}: {1}'.format('Warning', 'Project is not running.'))
            sys.exit(1)

        try:
            path = self.json_data[int(number) - 1]['path']
            subprocess.call('cd {0} && docker-compose down'.format(path), shell=True)
            self.cache.forget(number)
        except Exception as e:
            print("{0}: {1}".format('Error', e))
            sys.exit(1)

    def reset(self):
        subprocess.call('docker rm -vf $(docker ps -a -q)', shell=True)
        self.cache.forget()