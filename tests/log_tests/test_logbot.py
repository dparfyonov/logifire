"""
Test Logifire

Authors:
    Dmitry Parfyonov <parfyonov.dima@gmail.com>
"""

# import

import unittest
import logging

from logifire import Logifire, Logbranch
from cases import MockHandler

# TestLogifire

class TestLogifire(unittest.TestCase):
    def test_basic(self):
        mh = MockHandler()
        log = Logifire(
            name='Logifire_test',
            level=logging.DEBUG,
            branches=[Logbranch(mh)]
        )
        log.debug("Test {} message", 'debug')
        log.info("Test {level} message", level='info')
        log.critical("Test critical message")

        rlog = mh.get_log()
        self.assertEqual(len(rlog), 3)
        self.assertTrue('debug' in rlog[0])
        self.assertTrue('DEBUG' in rlog[0])
        self.assertTrue('info' in rlog[1])
        self.assertTrue('INFO' in rlog[1])
        self.assertTrue('critical' in rlog[2])
        self.assertTrue('CRITICAL' in rlog[2])

    def test_different_levels(self):
        mh1 = MockHandler()
        mh2 = MockHandler()
        log = Logifire(
            name='logifire_test',
            level=logging.DEBUG,
            branches=[Logbranch(mh1), Logbranch(mh2, level=logging.CRITICAL)]
        )
        log.debug("Test debug message")
        log.info("Test info message")
        log.critical("Test critical message")

        rlog1 = mh1.get_log()
        self.assertEqual(len(rlog1), 3)
        self.assertTrue('debug' in rlog1[0])
        self.assertTrue('info' in rlog1[1])
        self.assertTrue('critical' in rlog1[2])

        rlog2 = mh2.get_log()
        self.assertEqual(len(rlog2), 1)
        self.assertTrue('critical' in rlog2[0])
