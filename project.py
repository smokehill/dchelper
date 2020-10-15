import os
import sys
import subprocess
import json

from cache import Cache


class Project:

    file_path = 'projects.json'
    json_data = [] # data from projects.json
    cache = None

    def __init__(self):
        if os.path.isfile(self.file_path) == False and os.access(self.file_path, os.R_OK) == False:
            sys.exit('{0}: {1}'.format('Error', 'Check if projects.json exists and it\'s readable.'))

        with open(self.file_path) as f:
            self.json_data = json.load(f)

        # init cache
        self.cache = Cache()
        # self.cache.init()

    def list(self):
        proc_list = self.cache.proc_list
        i = 1
        for data in self.json_data:
            status = '\033[92m[+]\033[0m' if str(i) in proc_list else '\033[91m[-]\033[0m'
            n = ' ' + str(i) if len(self.json_data) < 100 and i < 10 else '' + str(i)
            print('{0} {1} {2}'.format(status, n, data['title']))
            i = i + 1

    def up(self):
        proc_list = self.cache.proc_list
        
        print('Project number:')
        number = raw_input('{0} '.format('>>>'))

        if number in proc_list:
            sys.exit('{0}: {1}'.format('Warning', 'Project is running.'))

        try:
            path = self.json_data[int(number) - 1]['path']
            subprocess.call('cd {0} && docker-compose up -d'.format(path), shell=True)
            self.cache.remember(number)
        except Exception as e:
            sys.exit("{0}: {1}".format('Error', e))

    def down(self):
        proc_list = self.cache.proc_list

        print('Project number:')
        number = raw_input('{0} '.format('>>>'))

        if number not in proc_list:
            sys.exit('{0}: {1}'.format('Warning', 'Project is not running.'))

        try:
            path = self.json_data[int(number) - 1]['path']
            subprocess.call('cd {0} && docker-compose down'.format(path), shell=True)
            self.cache.forget(number)
        except Exception as e:
            sys.exit("{0}: {1}".format('Error', e))

    def reset(self):
        subprocess.call('docker rm -vf $(docker ps -a -q)', shell=True)
        self.cache.forget()


if __name__ == '__main__':
    name = "Project"