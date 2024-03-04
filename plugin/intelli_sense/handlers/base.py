import logging

from ...config import Config

from ...base import FileSystem


class BaseHandler(object):

    def __init__(self, intelli_sense):
        self.intelli_sense = intelli_sense
        self.cfg = Config()
        self.fs = FileSystem(self.cfg)

        self.logger = logging.getLogger()
        self.debugger = logging.getLogger("debugger")
