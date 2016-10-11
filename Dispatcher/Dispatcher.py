#!/usr/bin/env python
"""Handles the queues, dispatching jobs

Blah, Blah
"""
import Queue

import constants
import copy


class Dispatcher(object):
    def __init__(self):
        """clears ready_Q and blocked_Q these are queues of PCB structures,
        initializes runningPCB to default values in constants (see PCB structure)"""
        self._readyQ = Queue.Queue()
        self._blockedQ = Queue.Queue()
        self._runningPCB = constants.PCB()
        self._runningPCB_valid = False

    def init(self):
        self.__init__()

    def add_job(self, my_pcb):
        """add a job to the ready queue"""
        self._readyQ.put(my_pcb)

    def switch_process(self):
        # if no jobs on the queue say so
        if self._readyQ.empty():
            if self._blockedQ.empty():
                return constants.NO_JOBS
            else:
                return constants.BLOCKED_JOBS

        # readyQ has jobs, get
        # and remove one from queue
        tmp = self._readyQ.get()

        # push current job onto stack if its still valid
        if self._runningPCB_valid:
            self._readyQ.put(self._runningPCB)

        # now make the tmp the new one
        self._runningPCB = tmp
        self._runningPCB_valid = True
        return constants.PCB_SWITCHED_PROCESSES

    def io_complete(self):
        b_moved_from_blocked_queue = False

        while not self._blockedQ.empty():
            tmpPCB = self._blockedQ.get()

            # set io time to zero to indicate that
            # we have already done our IO
            tmpPCB.io_time = 0
            self._readyQ.put(tmpPCB)
            b_moved_from_blocked_queue = True
        if b_moved_from_blocked_queue:
            return constants.PCB_MOVED_FROM_BLOCKED_TO_READY
        else:
            return constants.PCB_BLOCKED_QUEUE_EMPTY

    def process_interrupt(self, interrupt):
        """
        interrupt can be either;
        a switch process interrupt in which case the function performs the appropriate tasks and returns
        PCB_SWITCHED_PROCESSES or a io_complete interrupt in which case it pulls ALL processes off of the blockedQ and
        returns either PCB_MOVED_FROM_BLOCKED_TO_READY (if there were any) or PCB_BLOCKED_QUEUE_EMPTY if there were none
        """
        if interrupt == constants.SWITCH_PROCESS:
            return self.switch_process()
        elif interrupt == constants.IO_COMPLETE:
            return self.io_complete()
        else:
            return constants.PCB_UNIMPLEMENTED

    def get_current_job(self):
        """used for testing, return a copy of runningPCB"""
        return self._runningPCB

    def do_tick(self):
        """see if we are working on anything
        if nothing available say so
        otherwise try to load a new job"""
        if not self._runningPCB_valid:
            if self._readyQ.empty():
                if self._blockedQ.empty():
                    return constants.NO_JOBS
                else:
                    return constants.BLOCKED_JOBS
            else:
                # readyQ has jobs, load one
                self._runningPCB = self._readyQ.get()
                self._runningPCB_valid = True
                return constants.PCB_MOVED_FROM_READY_TO_RUNNING

        # so we are working on whats in myPCB
        # subtract 1 ticks worth of CPU time
        if self._runningPCB.cpu_time > 0:
            self._runningPCB.cpu_time -= 1

        if self._runningPCB.cpu_time == 0:
            i_retcode = constants.PCB_FINISHED

            if self._runningPCB.io_time > 0:
                # add it to the blocked queue
                self._blockedQ.put(copy.deepcopy(self._runningPCB))
                i_retcode = constants.PCB_ADDED_TO_BLOCKED_QUEUE

            # cheesy but indicates that we are done with this one
            self._runningPCB.process_number = constants.UNINITIALIZED
            self._runningPCB_valid = False
            return i_retcode
        else:
            return constants.PCB_CPUTIME_DECREMENTED
