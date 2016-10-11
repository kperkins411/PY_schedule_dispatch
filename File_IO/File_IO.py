#!/usr/bin/env python
"""Module for loading process data from a file

Loads and sorts by process start_time
You can either pop the next starting module  of the
container hosting it, or peek at when its supposed to start
"""
import constants
from operator import attrgetter


class File_IO(object):
    def __init__(self):
        """holds all the process control blocks (PCB)"""
        self._PCBList = []

    def load_data(self, filename=constants.DEFAULT_PCB_FILE):
        """attempt to open file 'filename' to read, parse its rows
        into PCB structs and add these structs to a vector
        returns SUCCESS if all goes well or COULD_NOT_OPEN_FILE
        Throws an IOError exception if file not found"""

        # clear list
        del self._PCBList[:]

        with open(filename, 'rt') as f:
            for line in f:
                # read and parse file into list
                cl = line.split(",")
                one_pcb = constants.PCB(cl[0], cl[1], cl[2], cl[3])
                self._PCBList.append(one_pcb)

            # sort list by start time, want the soonest start time last
            self._PCBList = sorted(self._PCBList, key=attrgetter('start_time'), reverse=True)
        return constants.SUCCESS

    def get_next(self):
        """return the first struct in the vector
        then deletes it from the vector
        throws IndexError if there are no jobs left"""
        return self._PCBList.pop()

    def peek_next_start_time(self):
        """returns when the next job starts without altering the container
        throws IndexError if there are no jobs"""
        return self._PCBList[-1].start_time

    def size(self):
        """ return the number of elements
        in the container"""
        return len(self._PCBList)

# try:
#     return self._PCBList[-1].start_time
# except IndexError:
#     return constants.NO_JOBS
# else:
#     # Handle task here and call q.task_done()
#     # return a PCB
#     return constants.SUCCESS
