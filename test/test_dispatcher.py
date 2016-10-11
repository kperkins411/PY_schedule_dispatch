import unittest
from Dispatcher.Dispatcher import Dispatcher
import constants


class Test_Dispatcher(unittest.TestCase):
    def setUp(self):
        self.dispatcher = Dispatcher()

    # test init()
    def test_init(self):
        self.dispatcher.init()
        self.assertTrue( self.dispatcher._readyQ.empty(),"_readyQ not empty")
        self.assertTrue(self.dispatcher._blockedQ.empty(), "_blockedQ not empty")
        self.assertTrue(self.dispatcher._runningPCB.io_time == constants.UNINITIALIZED)
        self.assertTrue(self.dispatcher._runningPCB.cpu_time == constants.UNINITIALIZED)
        self.assertTrue(self.dispatcher._runningPCB.process_number == constants.UNINITIALIZED)
        self.assertTrue(self.dispatcher._runningPCB.start_time == constants.UNINITIALIZED)
        self.assertTrue(self.dispatcher._runningPCB_valid == False)

    # add a job test size of queue make sure running_pcb is invalid
    def test_load_0_job(self):
        self.dispatcher.init()
        retval = self.dispatcher.do_tick()
        self.assertTrue(retval == constants.NO_JOBS)


    def initialize(self, has_io = 0):
        self.dispatcher.init()
        pcb = constants.PCB(0, 1, 1, has_io)
        self.dispatcher.add_job(pcb)
        self.assertTrue(self.dispatcher._readyQ.qsize() == 1, "_readyQ size is wrong")
        self.assertTrue(self.dispatcher._blockedQ.qsize() == 0, "_blockedQ size is wrong")

    def two_ticks(self,has_io):
        # should load into running process and set runningPCB_valid = True
        retval = self.dispatcher.do_tick()
        self.assertTrue(retval == constants.PCB_MOVED_FROM_READY_TO_RUNNING)

        pcb = self.dispatcher.get_current_job()
        self.assertTrue(pcb.io_time == has_io)
        self.assertTrue(pcb.cpu_time == 1)
        self.assertTrue(pcb.process_number == 0)
        self.assertTrue(pcb.start_time == 1)

        self.assertTrue(self.dispatcher._readyQ.qsize() == 0, "_readyQ size is wrong")
        self.assertTrue(self.dispatcher._blockedQ.qsize() == 0, "_blockedQ size is wrong")

        # should load into running process and set runningPCB_valid = True
        return( self.dispatcher.do_tick())

    def test_load_1_job_no_IO(self):
        self.initialize(has_io=0)

        retval = self.two_ticks(has_io=0)
        self.assertTrue(retval == constants.PCB_FINISHED)

    def test_load_1_job_has_IO(self):
        self.initialize(has_io=1)

        retval = self.two_ticks(has_io=1)

        #make sure its been moved to blocked queue
        self.assertTrue(retval == constants.PCB_ADDED_TO_BLOCKED_QUEUE)

        #force it out of blocked queue
        retval = self.dispatcher.process_interrupt(constants.IO_COMPLETE)

        # make sure its been moved from blocked to readyQ
        self.assertTrue(retval == constants.PCB_MOVED_FROM_BLOCKED_TO_READY)

        #moved to readyQ
        retval = self.dispatcher.do_tick()
        self.assertTrue(retval == constants.PCB_MOVED_FROM_READY_TO_RUNNING)

        retval = self.dispatcher.do_tick()
        self.assertTrue(retval == constants.PCB_FINISHED)


