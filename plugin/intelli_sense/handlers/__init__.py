from .functions import FunctionHandler
from .imports import ImportHandler

from ...base.types import PluginCommand


handlers = {
    PluginCommand.FUNCTION.value: FunctionHandler,
    PluginCommand.IMPORT.value: ImportHandler,
}


__all__ = [
    "FunctionHandler",
    "ImportHandler",
]
