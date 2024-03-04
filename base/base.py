from abc import abstractmethod
import os


class BaseConfigObject(object):

    def __init__(self, start_dir):
        self.start_dir = start_dir

    @property
    @abstractmethod
    def projects_names(self):
        raise NotImplementedError

    @property
    def working_dir(self):
        return os.path.join(self.start_dir, "work")

    @property
    def projects_dir(self):
        return os.path.join(self.start_dir, "projects")

    @property
    def service_path(self):
        return os.path.join(self.working_dir, "assistant")

    @property
    def log_folder(self):
        return os.path.join(self.service_path, "logs")

    @property
    @abstractmethod
    def project_logs_folders(self):
        raise NotImplementedError

    def get_project_logs_file_name(self, log_folder):
        return "errors.log"

    @property
    @abstractmethod
    def db_url(self):
        raise NotImplementedError

    def get_project_path(self, name):
        return os.path.join(self.working_dir, name)

    @property
    def projects(self):
        return {
            name: self.get_project_path(name)
            for name in self.projects_names
        }

    @property
    @abstractmethod
    def work_subfolders(self):
        raise NotImplementedError

    @property
    def flake_file(self):
        return "flake.log"

    @property
    def status_file(self):
        return "status.log"

    @property
    def wsl2win_dir(self):
        return "wsl2win"

    @property
    def wsl2win_queue(self):
        return "queue.txt"

    @property
    def npp_queue(self):
        return "queue_npp.txt"

    @property
    def excludes(self):
        return [
            self.wsl2win_dir,
            ".log",
            ".sql",
            "local",
            "flake8",
            "pylintrc",
        ]
