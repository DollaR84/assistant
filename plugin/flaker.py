import os

from Npp import editor, notepad, NOTIFICATION

from .base_plugin import BaseInstallPlugin

from .logger import setup_logger


setup_logger("flaker")


class Flaker(BaseInstallPlugin):

    def __install__(self):
        notepad.callback(self.check_file, [NOTIFICATION.FILEBEFORESAVE])

    def __uninstall__(self):
        notepad.clearCallbacks([NOTIFICATION.FILEBEFORESAVE])

    def __run__(self, name, file_path, **kwargs):
        if not file_path.endswith(".py"):
            return

        self.fs.write_queue(name, "flaker", file_path, **kwargs)
