import asyncio
import argparse
from functools import partial
import json
import logging
import os
from threading import Event
from queue import Queue

from base import FileSystem
from base.types import PluginCommand

from callback import CallbackData
from config import Config

from flaker import Flaker

from linter import Linter

from watcher import Watcher

from logger import setup_logger

from parser import Parser


setup_logger("assistant")


class Assistant:

    def __init__(self, config: Config, parser: Parser | None):
        self.cfg = config
        self.parser = parser
        self.fs = FileSystem(self.cfg)

        self.queue = Queue()
        self.event = Event()

        self.is_queue_modified: bool = False
        self.callback_value: str = None

        self.watcher = Watcher(self.queue)

    @property
    def is_parser(self):
        return bool(self.parser)

    async def parse(self):
        await self.parser.run()

    def callback_clear(self):
        self.is_queue_modified = False
        self.callback_value = None

    def callback_handler(self, data: CallbackData):
        param_name = f"is_{data.event_handler}_{data.event_type}"
        if hasattr(self, param_name):
            setattr(self, param_name, True)
            self.callback_value = data.value

    def finish(self):
        self.callback_clear()
        self.watcher.stop()

    def stop(self):
        self.event.set()


def __check_queue__(cfg: Config):
    lines, line = None, None
    for name, path in cfg.projects.items():
        with open(os.path.join(path, cfg.wsl2win_dir, cfg.wsl2win_queue), "r") as queue:
            lines = queue.readlines()

        if lines:
            line = lines[0]
            with open(os.path.join(path, cfg.wsl2win_dir, cfg.wsl2win_queue), "w") as queue:
                queue.writelines(lines[1:])
            break

    command, file_path = line.split(": ", 1) if line else (None, None,)
    return command, file_path


def check_queue(assistant: Assistant):
    try:
        return __check_queue__(assistant.cfg)
    except Exception as error:
        logging.error(error, exc_info=True)
        assistant.stop()


async def worker(assistant: Assistant):
    loop = asyncio.get_running_loop()
    check_queue_partial = partial(check_queue, assistant)

    while not assistant.event.is_set():
        if assistant.queue.qsize():
            data = assistant.queue.get()
            assistant.callback_handler(data)

            if not assistant.is_queue_modified:
                await asyncio.sleep(assistant.cfg.WORKER_TIMEOUT)
                continue

        command, data = await loop.run_in_executor(None, check_queue_partial)
        if data:
            data = json.loads(data)
            file_path = data.get("file_path")

        match command:
          case "flaker":
            await Flaker(file_path).run()
          case "linter":
              await Linter(file_path).run()
          case PluginCommand.IMPORT.value | PluginCommand.FUNCTION.value:
            pass
          case None:
            assistant.callback_clear()
            if assistant.is_parser:
                await assistant.parse()
                assistant.stop()
          case _:
            logger = logging.getLogger()
            logger.error(f"Unknown command: '{command}' read from queue. file_path: '{file_path}'")

        await asyncio.sleep(assistant.cfg.WORKER_TIMEOUT)

    assistant.finish()


def main():
    cfg = Config()

    cmd_parser = argparse.ArgumentParser(description="Service assistant for programming python projects")
    cmd_parser.add_argument(
        "-c", "--command",
        type=str, default=None,
        action="store", choices=["scan"],
        help="Command for run"
    )

    cmd_parser.add_argument(
        "-p", "--project_name",
        type=str, default=None,
        action="store", choices=cfg.projects_names,
        help="Set project name"
    )
    args = cmd_parser.parse_args()

    parser = None
    if args:
        parser = Parser(args)

    assistant = Assistant(cfg, parser)
    try:
        asyncio.run(worker(assistant))
    except KeyboardInterrupt:
        assistant.stop()


if "__main__" == __name__:
    main()
