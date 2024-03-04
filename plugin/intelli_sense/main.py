import logging

from .handlers import handlers

from ..base.types import PluginCommand

from ..config import Config


class IntelliSense(object):

    def __init__(self):
        self.cfg = Config()

        self.project_name = None
        self.module = None

        self.handlers = {
            command: handler(self)
            for command, handler in handlers.items()
        }

        self.logger = logging.getLogger("debugger")

    def run(self, command, file_path, selection_text, start_pos, end_pos):
        if command not in list(self.handlers.keys()):
            return
        self.project_name = None
        self.module = None

        file_path = self.cfg.restore_path(file_path)
        for name, path in self.cfg.projects.items():
            if path in file_path:
                self.project_name = name
                self.module = file_path.replace(path, "").strip("\\")
                break

        if not self.project_name:
            return

        subfolder = self.cfg.work_subfolders.get(self.project_name)
        if subfolder and self.module.startswith(subfolder):
            self.module = self.module.replace(subfolder, "").strip("\\")
        self.module = self.module.replace("\\", ".")
        if self.module.endswith(".py"):
            self.module = self.module[:-3]

        handler = self.handlers[command]
        handler.process(selection_text, start_pos, end_pos)
