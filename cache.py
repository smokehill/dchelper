import os

class Cache:

    __file = ''
    __proc_list = [] # contains projects numbers like processes ids

    def __init__(self):
        # init file
        self.__file = os.getcwd() + '/.cache'
        if os.path.isfile(self.__file) == False:
            f = open(self.__file, 'w')
            f.close()

        # fill proc_list
        f = open(self.__file, 'r')
        if f.readline() != '':
            f = open(self.__file, 'r')
            self.__proc_list = list(f.readline().split(' '))

    def remember(self, number):
        if str(number) not in self.__proc_list:
            self.__proc_list.append(str(number))
            f = open(self.__file, 'w')
            f.write(' '.join(self.__proc_list))
            f.close()

    def forget(self, number = None):
          if number is None:
              self.__proc_list = []
              os.remove(self.__file)
          else:
              if str(number) in self.__proc_list:
                  self.__proc_list.remove(str(number))
                  f = open(self.__file, 'w')
                  f.write(' '.join(self.__proc_list))
                  f.close()

    def get_proc_list(self):
        return self.__proc_list