import os


class Cache:

    file_path = ''
    proc_list = [] # projects numbers

    def __init__(self, f_name = None):
        if f_name is not None:
            self.file_path = os.path.dirname(__file__) + '/' + f_name
        else:
            self.file_path = os.path.dirname(__file__) + '/.cache'

        # init file
        if os.path.isfile(self.file_path) == False:
            f = open(self.file_path, 'w')
            f.close()

        # fill proc_list
        f = open(self.file_path, 'r')
        if f.readline() != '':
            f = open(self.file_path, 'r')
            self.proc_list = list(f.readline().split(' '))

    def remember(self, number):
        if str(number) not in self.proc_list:
            self.proc_list.append(str(number))
            f = open(self.file_path, 'w')
            f.write(' '.join(self.proc_list))
            f.close()

    def forget(self, number = None):
        if number is None and self.file_path != False:
            self.proc_list = []
            os.remove(self.file_path)

        else:
            if str(number) in self.proc_list:
                self.proc_list.remove(str(number))
                f = open(self.file_path, 'w')
                f.write(' '.join(self.proc_list))
                f.close()


if __name__ == '__main__':
    name = "Cache"