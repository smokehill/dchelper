import os
import sys
import subprocess


# Cache functions

cache_file = os.getcwd() + '/.cache'

def __remember(number):
    """Add project number into .cache file."""
    if os.path.isfile(cache_file) == False:
        f = open(cache_file, 'w')
        f.close()

    f = open(cache_file, 'r')
    if f.readline() == '':
        f = open(cache_file, 'w')
        f.write(str(number))
        f.close()

    else:
        proc_list = list(f.readline().split(' '))
        if str(number) not in proc_list:
            proc_list.append(str(number))
            f = open(cache_file, 'w')
            f.write(' '.join(proc_list))
            f.close()

def __forget(number = None):
    """Remove project number from .cache file."""
    if os.path.isfile(cache_file) == True:

        if number is None:
            os.remove(cache_file)

        else:
            f = open(cache_file, 'r')
            if f.readline() != '':
                f = open(cache_file, 'r')
                proc_list = list(f.readline().split(' '))

                if str(number) in proc_list:
                    proc_list.remove(str(number))
                    f = open(cache_file, 'w')
                    f.write(' '.join(proc_list))
                    f.close()

def __get_remembered():
    """Return projects numbers list from .cache file."""
    proc_list = []
    if os.path.isfile(cache_file) == True:
        f = open(cache_file, 'r')
        if f.readline() != '':
            f = open(cache_file, 'r')
            proc_list = list(f.readline().split(' '))
    return proc_list

# Wrappers for docker-compose

def list_projects(items):
    """List available projects."""
    proc_list = __get_remembered()

    i = 1
    for item in items:
        status = '\033[92m[+]\033[0m' if str(i) in proc_list else '\033[91m[-]\033[0m'
        print('{0} {1} {2}'.format(status, i, item['title']))
        i = i + 1

def dc_up(items):
    """Request number and up project containers."""
    proc_list = __get_remembered()
    
    print('Project number:')
    number = raw_input('{0} '.format('>>>'))

    if number in proc_list:
        sys.exit('{0}: {1}'.format('Warning', 'Project is running.'))

    try:
        project_path = items[int(number) - 1]['path']
        subprocess.call('cd {0} && docker-compose up -d'.format(project_path), shell=True)
        __remember(number)
    except Exception as e:
        sys.exit("{0}: {1}".format('Error', e))

def dc_down(items):
    """Request number and down project containers."""
    proc_list = __get_remembered()

    print('Project number:')
    number = raw_input('{0} '.format('>>>'))

    if number not in proc_list:
        sys.exit('{0}: {1}'.format('Warning', 'Project is not running.'))

    try:
        project_path = items[int(number) - 1]['path']
        subprocess.call('cd {0} && docker-compose down'.format(project_path), shell=True)
        __forget(number)
    except Exception as e:
        sys.exit("{0}: {1}".format('Error', e))

def dc_reset():
    """Reset all projects containers."""
    subprocess.call('docker rm -vf $(docker ps -a -q)', shell=True)
    __forget()