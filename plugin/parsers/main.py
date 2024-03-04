import logging

from .parsers import BaseParser

from ..config import Config


class Parser(object):

    def __init__(self, assistant):
        self.assistant = assistant
        self.cfg = Config()

    def parse(self):
        try:
            parser = BaseParser.get(self.assistant)
            parser.parse()
        except Exception as error:
            logging.error(error, exc_info=True)
