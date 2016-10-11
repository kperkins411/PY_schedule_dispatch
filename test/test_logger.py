import unittest

import constants
from Logger import Logger


class Test_Logger(unittest.TestCase):
    def setUp(self):
        self._logger = Logger.Logger()

    def compare(self):
        i = 0
        with open(constants.LOGGER_TEST, 'rt') as f:
            for line in f:
                # read and parse file into list
                cl = line.strip("\n").split(",")
                self.assertEqual(int(cl[0]), self._logger._list[i][0], "first value wrong")
                self.assertEqual(int(cl[1]), self._logger._list[i][1], "second value wrong")
                i += 1

    # test
    def test_0(self):
        self._logger.save(filename=constants.LOGGER_TEST)
        self.compare()

    def test_1(self):
        testlist = [(1,2)]
        self._logger.log(1,2)
        self._logger.save(filename=constants.LOGGER_TEST)
        self.compare()

    def test_3(self):
        testlist = [(1,2),(3,4),(5,6)]
        self._logger.log(1,2)
        self._logger.log(3,4)
        self._logger.log(5,6)
        self._logger.save(filename=constants.LOGGER_TEST)
        self.compare()





