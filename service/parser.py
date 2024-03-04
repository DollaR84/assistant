import logging

from config import Config

from scanner import Scanner


class Parser:

    def __init__(self, args):
        self.args = args
        self.cfg = Config()

        self.command = self.args.command
        self.project_name = self.args.project_name

        self.logger = logging.getLogger("warnings")

    async def run(self):
        match self.command:
          case "scan":
            if not self.cfg.projects.get(self.project_name):
                self.logger.warning(f"Unknown project_name: '{self.project_name}'")
                return

            await Scanner(self.project_name).run()
          case None:
            pass
          case _:
            self.logger.warning(f"Unknown command: '{self.command}' read from cmd. project_name: '{self.project_name}'")
