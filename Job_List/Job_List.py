#!/usr/bin/env python
"""Module feeding jobs to dispatcher as they become available

"""
import constants
from File_IO import File_IO


class Job_List(object):
    def __init__(self):
        self.job_list_has_jobs = False
        self.file_io = File_IO.File_IO()

    def init(self, filename=constants.DEFAULT_PCB_FILE):
        # load data
        try:
            ret = self.file_io.load_data(filename)
        except IOError:
            return constants.COULD_NOT_OPEN_FILE

        # no jobs then bail
        if self.file_io.size() == 0:
            return constants.NO_JOBS

        # so we have at least 1 job to run
        self.job_list_has_jobs = True
        return  ret

    def get_next_job(self):
        return self.file_io.get_next()

    def do_tick(self, currentTick):
        if not self.job_list_has_jobs:
            return constants.NO_JOBS
        try:
            next_start_time = self.file_io.peek_next_start_time()
        except IndexError:
            next_start_time = constants.NO_JOBS

        if next_start_time == constants.NO_JOBS:
            self.job_list_has_jobs = False
            return constants.NO_JOBS

        # see if its time to add this job
        if next_start_time <= currentTick:
            # handle the case of multiple jobs starting at same time
            # doTick(currentTick);
            return constants.ADD_JOB_TO_DISPATCHER
        else:
            return constants.WAITING_TO_ADD_JOB_TO_DISPATCHER
