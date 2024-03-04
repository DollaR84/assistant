import asyncio
import logging
import os

from config import Config

from logger import setup_logger


setup_logger("flaker")


class Flaker:

    def __init__(self, file_path: str):
        self.cfg = Config()
        self.file_path: str = self.cfg.restore_path(file_path)

    def get_project_path(self):
        project_path = None
        for path in self.cfg.projects.values():
            if path in self.file_path:
                project_path = path
                break
        return project_path

    async def __run__(self):
        project_path = self.get_project_path()
        if not project_path:
            return

        flake_command = [f"{self.cfg.env_path}flake8", self.file_path]
        flake_path = os.path.join(project_path, self.cfg.flake_file)
        with open(flake_path, "w") as flake_file:
            await asyncio.create_subprocess_exec(*flake_command, cwd=project_path, stdout=flake_file, shell=False)

    async def run(self):
        try:
            await self.__run__()
        except Exception as error:
            logging.error(error, exc_info=True)
