#!/usr/bin/env python
"""Runs the fileIO and scheduler
"""
import constants
from Job_List import Job_List
from Dispatcher import Dispatcher
from Logger import Logger
import Plot_Process.plot_processes

TIMESLICE = 4
NUMBER_CYCLES_BETWEEN_IO_INTERRUPTS = 20


def main():
    timeslice_time_used = constants.TIMER_BEGIN
    tickcount = constants.TIMER_BEGIN

    switch_process = False
    jobs_waiting_for_io_interrupt = False
    show_job_list_empty_message = True

    # for jobs and to simulate job execution
    joblist = Job_List.Job_List()
    dispatcher = Dispatcher.Dispatcher()
    logger = Logger.Logger()

    #if you cannot load any jobs you have nothing to do
    ret = joblist.init(filename=constants.DEFAULT_PCB_FILE)
    if ret != constants.SUCCESS:
        return ret

    finished = False
    while not finished:
        tickcount += 1
        timeslice_time_used += 1

        # are there jobs on the blocked_Q that need an interrupt to wake them?
        # if so then periodically set this interrupt off to clear them
        if jobs_waiting_for_io_interrupt:
            if tickcount % NUMBER_CYCLES_BETWEEN_IO_INTERRUPTS == 0:
                # ignore the return code, not printing anything
                dispatcher.process_interrupt(constants.IO_COMPLETE)
                jobs_waiting_for_io_interrupt = False

        # do joblist stuff, dont add all jobs that should start now
        i_ret_jobs = joblist.do_tick(tickcount)
        while i_ret_jobs == constants.ADD_JOB_TO_DISPATCHER:
            # a job is ready pull from joblist and add to dispatcher
            new_job = joblist.get_next_job()
            dispatcher.add_job(new_job)
            i_ret_jobs = joblist.do_tick(tickcount)

        # do dispatcher stuff
        i_ret_dispatcher = dispatcher.do_tick()
        if i_ret_dispatcher == constants.PCB_FINISHED:
            # if finished give up rest of timeslice!!!!
            timeslice_time_used = 0
        elif i_ret_dispatcher == constants.PCB_ADDED_TO_BLOCKED_QUEUE:
            jobs_waiting_for_io_interrupt = True
            # if blocked give up rest of timeslice!!!!
            timeslice_time_used = 0
        # elif i_ret_dispatcher == constants.PCB_MOVED_FROM_READY_TO_RUNNING:
        #     jobs_waiting_for_io_interrupt = True
        #     #if blocked give up rest of timeslice!!!!
        #     timeslice_time_used = 0;

        # computes the remainder of tickcount % TimeSlice
        # if 0 then time to switch
        if timeslice_time_used % TIMESLICE == 0:
            timeslice_time_used = 0
            dispatcher.process_interrupt(constants.SWITCH_PROCESS)

        # we are done when no more jobs
        finished = (i_ret_jobs == constants.NO_JOBS and i_ret_dispatcher == constants.NO_JOBS)

        # if everything is done do not log the event
        if not finished:
            logger.log(tickcount, dispatcher.get_current_job().process_number)

    logger.save()
    return constants.SUCCESS


if __name__ == '__main__':
    ret = main()

    if ret  == constants.SUCCESS:
        Plot_Process.plot_processes.plot()
    elif ret == constants.COULD_NOT_OPEN_FILE:
        print("Cannot open input file, is testdata.txt in right directory?")
    elif ret == constants.NO_JOBS:
        print("No jobs to process")


