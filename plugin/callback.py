from collections import namedtuple


class CallbackData(namedtuple("CallbackData", ["event_handler", "event_type", "value"])):
    __slots__ = ()
    def __new__(cls, event_handler, event_type, value=None):
        return super(CallbackData, cls).__new__(cls, event_handler, event_type, value)
