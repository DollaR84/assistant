import json
import logging
from threading import Event, Thread
from Queue import Queue
import os

from Npp import notepad, NOTIFICATION

from .base_plugin import BaseInstallPlugin

from .config import Config

from .intelli_sense import IntelliSense
from .base.types import PluginCommand

from .parsers import Parser

from .watcher import Watcher

from .logger import setup_logger


setup_logger("assistant")


class Assistant(BaseInstallPlugin):

    def __init__(self):
        super(Assistant, self).__init__()
        self.parser = Parser(self)
        self.intelli_sense = IntelliSense()

        self.is_status_modified = False
        self.callback_value = None

        self.queue = Queue()
        self.event = Event()
        self.thread = None
        self.start()

        self.watcher = Watcher(self.queue)

    def __install__(self):
        notepad.callback(self.run, [NOTIFICATION.SHUTDOWN])

    def __uninstall__(self):
        notepad.clearCallbacks([NOTIFICATION.SHUTDOWN])

    def callback_clear(self):
        self.is_status_modified = False
        self.callback_value = None

    def callback_handler(self, data):
        param_name = "_".join(["is", data.event_handler, data.event_type])
        if hasattr(self, param_name):
            setattr(self, param_name, True)

        self.callback_value = data.value
        self.parser.parse()

    def run(self, name, file_path):
        self.stop()

    def start(self):
        self.thread = Thread(target=__worker__, args=(self,))
        self.thread.start()

    def finish(self):
        self.callback_clear()
        self.watcher.stop()
        self.thread.stop()

    def stop(self):
        self.event.set()


def __check_queue__(cfg):
    lines, line = None, None
    for name, path in cfg.projects.items():
        with open(os.path.join(path, cfg.wsl2win_dir, cfg.npp_queue), "r") as queue:
            lines = queue.readlines()

        if lines:
            line = lines[0]
            with open(os.path.join(path, cfg.wsl2win_dir, cfg.npp_queue), "w") as queue:
                queue.writelines(lines[1:])
            break

    command, file_path = line.split(": ", 1) if line else (None, None,)
    return command, file_path


def check_queue(assistant):
    try:
        return __check_queue__(assistant.cfg)
    except Exception as error:
        logging.error(error, exc_info=True)
        assistant.stop()


def check_commands(assistant):
    command, data = check_queue(assistant)
    if data:
        data = json.loads(data)

    if command in [plugin_command.value for plugin_command in PluginCommand]:
        assistant.intelli_sense.run(command, **data)


def __worker__(assistant):
    while not assistant.event.isSet():
        try:
            if assistant.queue.qsize():
                data = assistant.queue.get()
                assistant.callback_handler(data)
                assistant.event.wait(assistant.cfg.REPEAT_TIMEOUT)
                continue

            check_commands(assistant)
            assistant.event.wait(assistant.cfg.REPEAT_TIMEOUT)
        except Exception as error:
            logging.error(error, exc_info=True)
            assistant.stop()

            assistant.finish()
