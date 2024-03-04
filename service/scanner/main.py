import logging

from config import Config

from db import crud

from .loader import DataLoader

from .saver import DataSaver


class Scanner:

    def __init__(self, project_name: str):
        self.cfg = Config()
        self.project_name = project_name

        self.loader = DataLoader(self.project_name)
        self.saver = DataSaver(self.project_name)

        self.logger = logging.getLogger("debugger")

    async def get_project(self, name: str, path: str):
        project = crud.get_project(name)
        if not project:
            project = crud.create_project(name, path, self.cfg.work_subfolders.get(name))
        return project

    async def run(self):
        path = self.cfg.projects[self.project_name]
        project = await self.get_project(self.project_name, path)

        try:
            data = self.loader.get_data()
            await self.process_data(project, data)
        except Exception as error:
            logging.error(error, exc_info=True)

    async def process_data(self, project, data):
        self.saver.set_project(project)
        await self.saver.save(data)
