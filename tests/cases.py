"""
Test cases

Authors:
    Dmitry Parfyonov <parfyonov.dima@gmail.com>
"""

# import

import logging

# MockHandler

class MockHandler(logging.Handler):

    def __init__(self, level: int = logging.NOTSET):
        """
        Init.
        Args:
            level: log level
        """
        super(MockHandler, self).__init__(level)
        self.__log = []

    def emit(self, record: logging.LogRecord):
        """
        Emit record.
        Args:
            record: log record
        """
        try:
            self.__log.append(self.format(record))
        except Exception:
            self.handleError(record)

    def get_log(self) -> list:
        """
        Get log.
        """
        return self.__log
