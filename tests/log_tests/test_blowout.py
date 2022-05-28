"""
Test Logifire

Authors:
    Dmitry Parfyonov <parfyonov.dima@gmail.com>
"""

# import

import os
import time
import unittest
import logging
from os.path import dirname, realpath, join

from logifire import Logifire, Logbranch
from logifire.blowout import BlowoutFile, BlowoutMemcached
from cases import MockHandler

# TestBlowout

class TestBlowout(unittest.TestCase):
    def test_process_backend(self):
        blowout_seconds = 0.1
        mh = MockHandler()
        log = Logifire(
            name='logifire_test',
            level=logging.DEBUG,
            branches=[Logbranch(mh, blowout_seconds=blowout_seconds)]
        )
        log.debug("Test debug message")
        log.info("Test info message")
        log.critical("Test critical message")

        rlog = mh.get_log()
        self.assertEqual(len(rlog), 1)
        self.assertTrue('debug' in rlog[0])

        time.sleep(blowout_seconds)
        log.info("Test info message")
        self.assertEqual(len(rlog), 2)
        self.assertTrue('info' in rlog[1])

    def test_file_source(self):
        blowout_seconds = 0.2
        curr_dir = dirname(realpath(__file__))
        log_file = join(curr_dir, '../tmp', 'log')
        if os.path.isfile(log_file):
            os.remove(log_file)

        fh = logging.FileHandler(log_file)
        lpf = Logbranch(fh, blowout_seconds=blowout_seconds, level=logging.INFO)
        mh = MockHandler()
        bof = BlowoutFile()
        log = Logifire(
            name='logifire_test',
            level=logging.DEBUG,
            branches=[
                Logbranch(mh),
                lpf,
            ],
            blowout=bof
        )
        log.debug("Test debug message")
        log.info("Test info1 message")

        blowout_file = bof.get_filename(lpf.get_handler_id())
        self.assertTrue(os.path.isfile(blowout_file))

        # run log in the other process
        cmd = 'python {script} {file} {log_level} "{message}" {message_level} {bo_source}:{bo_seconds}'.format(
            script=join(curr_dir, '../write_file_log.py'),
            file=log_file,
            log_level=logging.INFO,
            message="Test info2 message",
            message_level=logging.INFO,
            bo_source='file',
            bo_seconds=blowout_seconds
        )
        os.system(cmd)

        with open(log_file, 'r') as f:
            rlog = f.readlines()
            self.assertEqual(len(rlog), 1)
            self.assertTrue('info1' in rlog[0])

        rlog = mh.get_log()
        self.assertEqual(len(rlog), 2)
        self.assertTrue('debug' in rlog[0])
        self.assertTrue('info1' in rlog[1])

        time.sleep(blowout_seconds)

        # run log again in the other process
        os.system(cmd)

        with open(log_file, 'r') as f:
            rlog = f.readlines()
            self.assertEqual(len(rlog), 2)
            self.assertTrue('info2' in rlog[1])

        os.remove(log_file)

    def test_memcached_source(self):
        blowout_seconds = 1
        curr_dir = dirname(realpath(__file__))
        log_file = join(curr_dir, '../tmp', 'log')
        if os.path.isfile(log_file):
            os.remove(log_file)

        fh = logging.FileHandler(log_file)
        mh = MockHandler()
        bomc = BlowoutMemcached()
        log = Logifire(
            name='logifire_test',
            level=logging.DEBUG,
            branches=[
                Logbranch(mh),
                Logbranch(fh, blowout_seconds=blowout_seconds, level=logging.INFO)
            ],
            blowout=bomc
        )
        log.debug("Test debug message")
        log.info("Test info1 message")

        # run log in the other process
        cmd = 'python {script} {file} {log_level} "{message}" {message_level} {bo_source}:{bo_seconds}'.format(
            script=join(curr_dir, '../write_file_log.py'),
            file=log_file,
            log_level=logging.INFO,
            message="Test info2 message",
            message_level=logging.INFO,
            bo_source='memcached',
            bo_seconds=blowout_seconds
        )
        os.system(cmd)

        with open(log_file, 'r') as f:
            rlog = f.readlines()
            self.assertEqual(len(rlog), 1)
            self.assertTrue('info1' in rlog[0])

        rlog = mh.get_log()
        self.assertEqual(len(rlog), 2)
        self.assertTrue('debug' in rlog[0])
        self.assertTrue('info1' in rlog[1])

        time.sleep(blowout_seconds)

        # run log again in the other process
        os.system(cmd)

        with open(log_file, 'r') as f:
            rlog = f.readlines()
            self.assertEqual(len(rlog), 2)
            self.assertTrue('info2' in rlog[1])

        os.remove(log_file)
