import os
import sys
import subprocess
import json

from cache import Cache


cache = Cache()

class Project:

    __file = ''
    __json_data = []

    def __init__(self):
        self.__file = os.getcwd() + '/projects.json'
        if os.path.isfile(self.__file) == False and os.access(self.__file, os.R_OK) == False:
            sys.exit('{0}: {1}'.format('Error', 'Check if projects.json exists and it\'s readable.'))

        with open(self.__file) as f:
            self.__json_data = json.load(f)

    def list(self):
        proc_list = cache.get_proc_list()
        i = 1
        for data in self.__json_data:
            status = '\033[92m[+]\033[0m' if str(i) in proc_list else '\033[91m[-]\033[0m'
            n = ' ' + str(i) if len(self.__json_data) < 100 and i < 10 else '' + str(i)
            print('{0} {1} {2}'.format(status, n, data['title']))
            i = i + 1

    def up(self):
        proc_list = cache.get_proc_list()
        
        print('Project number:')
        number = raw_input('{0} '.format('>>>'))

        if number in proc_list:
            sys.exit('{0}: {1}'.format('Warning', 'Project is running.'))

        try:
            path = self.__json_data[int(number) - 1]['path']
            subprocess.call('cd {0} && docker-compose up -d'.format(path), shell=True)
            cache.remember(number)
        except Exception as e:
            sys.exit("{0}: {1}".format('Error', e))

    def down(self):
        proc_list = cache.get_proc_list()

        print('Project number:')
        number = raw_input('{0} '.format('>>>'))

        if number not in proc_list:
            sys.exit('{0}: {1}'.format('Warning', 'Project is not running.'))

        try:
            path = self.__json_data[int(number) - 1]['path']
            subprocess.call('cd {0} && docker-compose down'.format(path), shell=True)
            cache.forget(number)
        except Exception as e:
            sys.exit("{0}: {1}".format('Error', e))

    def reset(self):
        subprocess.call('docker rm -vf $(docker ps -a -q)', shell=True)
        cache.forget()