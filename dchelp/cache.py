import os


class Cache:

    proc_file = ''
    proc_list = []

    def __init__(self, name = None):
        name = name if name is not None else 'proc'
        cache_dir = os.path.expanduser('~') + '/.cache/dchelp'

        # create cache dir
        if os.path.isdir(cache_dir) == False:
            try:
                os.makedirs(cache_dir)
            except OSError:
                raise OSError(2, cache_dir + ' not exists.')

        # init proc_file
        self.proc_file = cache_dir + '/' + name
        if os.path.isfile(self.proc_file) == False:
            f = open(self.proc_file, 'w')
            f.close()

        # fill proc_list
        f = open(self.proc_file, 'r')
        if f.readline() != '':
            f = open(self.proc_file, 'r')
            self.proc_list = list(f.readline().split(' '))

    def remember(self, number):
        if str(number) not in self.proc_list:
            self.proc_list.append(str(number))
            f = open(self.proc_file, 'w')
            f.write(' '.join(self.proc_list))
            f.close()

    def forget(self, number = None):
        if number is None and self.proc_file != False:
            self.proc_list = []
            os.remove(self.proc_file)
        else:
            if str(number) in self.proc_list:
                self.proc_list.remove(str(number))
                f = open(self.proc_file, 'w')
                f.write(' '.join(self.proc_list))
                f.close()