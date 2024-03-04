from abc import abstractmethod
import logging
import os
import time

from Npp import editor, notepad

from .base import FileSystem

from .config import Config


class BasePlugin(object):

    def __init__(self):
        self.cfg = Config()
        self.fs = FileSystem(self.cfg)

    @abstractmethod
    def __run__(self, name, file_path, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def process_selection(self, file, selection_text, start_pos, end_pos):
        raise NotImplementedError

    def run(self, name, file_path, **kwargs):
        for _ in range(self.cfg.REPEAT_COUNT):
            try:
                self.__run__(name, file_path, **kwargs)
            except Exception as error:
                logging.error(error, exc_info=True)
                time.sleep(self.cfg.REPEAT_TIMEOUT)
            else:
                break

    def check_file(self, args):
        current_file = notepad.getCurrentFilename()
        for name, path in self.cfg.projects.items():
            if path in current_file:
                for exclude in self.cfg.excludes:
                    if exclude in current_file:
                        break
                else:
                    self.run(name, current_file)

    def check_selection(self):
        current_file = notepad.getCurrentFilename()

        num_selections = editor.getSelections()
        start_pos, end_pos = editor.getSelectionNStart(0), editor.getSelectionNEnd(0)

        if num_selections == 1 and start_pos != end_pos:
            selection_text = editor.getSelText()
            self.process_selection(current_file, selection_text, start_pos, end_pos)


class BaseInstallPlugin(BasePlugin):

    def __init__(self):
        super(BaseInstallPlugin, self).__init__()

        self.is_installed = False
        self.install()

    def install(self):
        if not self.is_installed:
            self.__install__()
            self.is_installed = True

    def uninstall(self):
        self.__uninstall__()
        self.is_installed = False

    @abstractmethod
    def __install__(self):
        raise NotImplementedError

    @abstractmethod
    def __uninstall__(self):
        raise NotImplementedError
