import logging
import os

from .base import BaseParser

from ...utils import GitStatus


class StatusParser(BaseParser):
    _is_status_modified = False

    def check(self):
        return self.assistant.is_status_modified

    def parse(self):
        if not StatusParser._is_status_modified:
            StatusParser._is_status_modified = True
            self.assistant.callback_clear()
            return
        StatusParser._is_status_modified = False

        logger = logging.getLogger("debugger")
        logger.debug("Run parser: {name}".format(name=self.name))

        for project_name, path in self.cfg.projects.items():
            if path in self.assistant.callback_value:
                project_path = path
                break
        else:
            project_path = None

        if project_path:
            files = []
            status_path = os.path.join(project_path, self.cfg.status_file)
            with open(status_path, "r") as status_file:
                try:
                    data = GitStatus(status_file.read())
                except Exception as error:
                    logging.error(error, exc_info=True)
                    data = None

                self.parse_data(project_name, data)

        self.assistant.callback_clear()
        logger.debug("finish parser: {name}".format(name=self.name))

    def parse_data(self, project_name, data):
        if not data:
            return
        rows = []

        rows.extend(self.parse_added(data.A))
        rows.extend(self.parse_deleted(data.D))
        rows.extend(self.parse_modified(data.M))
        rows.extend(self.parse_renamed(data.R))
        rows.extend(self.parse_untracked(data.untracked))

        self.run(project_name, rows)

    def parse_added(self, data):
        return data

    def parse_deleted(self, data):
        return data

    def parse_modified(self, data):
        return data

    def parse_renamed(self, data):
        return data

    def parse_untracked(self, data):
        results = []
        for row in data:
            for exclude in self.cfg.excludes:
                if exclude in row:
                    continue
                results.append(row)
        return results

    def run(self, project_name, rows):
        if not rows:
            return

        for row in rows:
            self.assistant.fs.write_queue(project_name, "linter", row)
