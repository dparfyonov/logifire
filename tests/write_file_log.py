#!/usr/bin/env python
"""
Write message to file log for tests.

Run:
    python write_file_log.py <log_file(str)> <log_level(int)> <log_message(str)> <message_level(int)> \
        [<blowout_source(file, memcache):blowout_seconds(float)>]

Authors:
    Dmitry Parfyonov <parfyonov.dima@gmail.com>
"""

# import

import sys
import logging

from os.path import dirname, realpath, join
sys.path.append(join(dirname(dirname(realpath(__file__))), 'src'))

from logifire import Logifire, Logbranch
from logifire.blowout import BlowoutFile, BlowoutMemcached


def main():
    """
    Main.
    """
    assert len(sys.argv) >= 5, \
        "run: python write_file_log.py <log_file(str)> <log_level(int)> <log_message(str)> <message_level(int)> " \
        "[<blowout_source(file, memcache):blowout_seconds(float)>]"

    log_file = sys.argv[1]
    log_level = int(sys.argv[2])
    log_message = sys.argv[3]
    message_level = int(sys.argv[4])

    blowout = None
    blowout_seconds = 0
    if len(sys.argv) > 5:
        blowout_source = sys.argv[5].split(':')
        assert blowout_source[0] in ('file', 'memcached')

        blowout_seconds = float(blowout_source[1])
        if blowout_source[0] == 'file':
            blowout = BlowoutFile()
        else:
            blowout = BlowoutMemcached()
            blowout_seconds = int(blowout_seconds)

    lb = Logifire(
        name='logifire_test',
        level=log_level,
        branches=[
            Logbranch(logging.FileHandler(log_file), log_level, blowout_seconds=blowout_seconds)
        ],
        blowout=blowout
    )
    lb.log(message_level, log_message)

# run

if __name__ == '__main__':
    main()
