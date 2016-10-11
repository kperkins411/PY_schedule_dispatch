#!/usr/bin/env python
"""simple list based log util

keeps all info (tickcount, process_number) in a list
saves when ready
"""
import constants
from operator import attrgetter

class Logger(object):
    def __init__(self):
        """holds all the process control blocks (PCB)"""
        self._list = []

    def log(self,tickcount, process_number):
        self._list.append((tickcount, process_number))

    def save(self,filename = constants.LOG_FILE):
        try:
            with open(filename, 'w') as outfile:
                for item in self._list:
                    outfile.write(str(item[0]) + "," + str(item[1]) +"\n")
        except IOError:
            print 'oops!'

        #try:
        # file = open(filename, 'w')
        #     try:
        #         for item in self._list:
        #             file.writelines(str(item[0]) + "," + str(item[1]))
        #     finally:
        #         file.close()
        # except IOError:
        #     print 'oops!'
