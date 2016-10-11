import unittest
from File_IO.File_IO import File_IO


class TestFile_IO(unittest.TestCase):
    def setUp(self):
        self.mfio = File_IO()

    # test size()
    def test_size_NOFILE(self):
        self.assertEquals(self.mfio.size(), 0)

    # test loading the file
    def test_loadData_NOFILE(self):
        with self.assertRaises(IOError):
            self.mfio.load_data()

    def test_loadData_TD0(self):
        self.mfio.load_data("td0.txt")
        self.assertEquals(self.mfio.size(), 0)

    def test_loadData_TD1(self):
        self.mfio.load_data("td1_withIO.txt")
        self.assertEquals(self.mfio.size(), 1)

    def test_loadData_TD9(self):
        self.mfio.load_data("td9_withIO.txt")
        self.assertEquals(self.mfio.size(), 9)

    # test getnext
    def test_getNext_no_entries(self):
        self.mfio.load_data("td0.txt")
        with self.assertRaises(IndexError):
            pcb = self.mfio.get_next()

    def test_getNext_1_entry(self):
        self.mfio.load_data("td1_withIO.txt")
        pcb = self.mfio.get_next()
        self.assertEquals(pcb.process_number, 1)
        self.assertEquals(pcb.start_time, 10)
        self.assertEquals(pcb.cpu_time, 7)
        self.assertEquals(pcb.io_time, 1)

        self.assertEquals(self.mfio.size(), 0)

        with self.assertRaises(IndexError):
            pcb = self.mfio.get_next()

    def test_getNext_9_entry(self):
        self.mfio.load_data("td9_withIO.txt")

        self.assertEquals(self.mfio.size(), 9)
        pcb = self.mfio.get_next()
        self.assertEquals(pcb.process_number, 6)
        self.assertEquals(pcb.start_time, 0)
        self.assertEquals(pcb.cpu_time, 4)
        self.assertEquals(pcb.io_time, 0)

        self.assertEquals(self.mfio.size(), 8)
        pcb = self.mfio.get_next()
        self.assertEquals(pcb.process_number, 9)
        self.assertEquals(pcb.start_time, 1)
        self.assertEquals(pcb.cpu_time, 6)
        self.assertEquals(pcb.io_time, 1)
        self.assertEquals(self.mfio.size(), 7)

    # test peek_next_start_time
    def test_peekNextStartTime_no_entries(self):
        self.mfio.load_data("td0.txt")
        with self.assertRaises(IndexError):
            st = self.mfio.peek_next_start_time()

    def test_peekNextStartTime_1_entry(self):
        self.mfio.load_data("td1_withIO.txt")
        self.assertEquals(self.mfio.size(), 1)
        self.assertEquals(self.mfio.peek_next_start_time(), 10)
        self.assertEquals(self.mfio.size(), 1)

    def test_peekNextStartTime_9_entry(self):
        self.mfio.load_data("td9_withIO.txt")

        self.assertEquals(self.mfio.size(), 9)
        self.assertEquals(self.mfio.peek_next_start_time(), 0)
        self.assertEquals(self.mfio.size(), 9)
