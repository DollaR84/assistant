from abc import abstractmethod

from ...config import Config


class MetaParser(type):

    def __new__(mcs, name, bases, attrs):
        cls = super(MetaParser, mcs).__new__(mcs, name, bases, attrs)

        name_ = name.lower().replace("parser", "")
        if name_ != "base":
            cls.register(name_)
        return cls


class BaseParser(object):
    __metaclass__ = MetaParser
    _parsers = {}

    @classmethod
    def register(cls, name):
        if cls._parsers is None:
            cls._parsers = {}

        cls._parsers[name] = cls

    @classmethod
    def get_by_name(cls, name):
        parser = cls._parsers.get(name)
        if not parser:
            raise TypeError("Error! Parser with name: {name} does not exist".format(name=name))
        return parser

    @classmethod
    def get(cls, assistant):
        for parser_cls in cls._parsers.values():
            parser = parser_cls(assistant)
            if parser.check():
                break
        else:
            parser = None

        if not parser:
            raise TypeError("Error! No parsers were found for the condition")
        return parser

    def __init__(self, assistant):
        self.assistant = assistant
        self.cfg = Config()

    @property
    def name(self):
        return self.__class__.__name__.lower().replace("parser", "")

    @abstractmethod
    def check(self):
        raise NotImplementedError

    @abstractmethod
    def parse(self):
        raise NotImplementedError
