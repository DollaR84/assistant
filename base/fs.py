import logging
import json
import os


class FileSystem(object):

    def __init__(self, config):
        self.cfg = config
        self.initialise()

    def makedirs(self, folder):
        try:
            os.makedirs(folder, exist_ok=True)
        except Exception as error:

            if not os.path.exists(folder):
                try:
                    os.makedirs(folder)
                except Exception as error:
                    logging.error(error, exc_info=True)

    def initialise(self):
        try:
            self.__initialise__()
        except Exception as error:
            logging.error(error, exc_info=True)

    def __initialise__(self):
        for project_path in self.cfg.projects.values():
            wsl2win_path = os.path.join(project_path, self.cfg.wsl2win_dir)
            self.makedirs(wsl2win_path)

            wsl2win_queue = os.path.join(wsl2win_path, self.cfg.wsl2win_queue)
            if not os.path.isfile(wsl2win_queue):
                with open(wsl2win_queue, "w"):
                    pass

            npp_queue = os.path.join(wsl2win_path, self.cfg.npp_queue)
            if not os.path.isfile(npp_queue):
                with open(npp_queue, "w"):
                    pass

    def write_queue(self, project_name, command, file_path, **kwargs):
        is_npp_queue = kwargs.pop("is_npp_queue", False)

        path = self.cfg.projects[project_name]
        if is_npp_queue:
            queue_path = os.path.join(path, self.cfg.wsl2win_dir, self.cfg.npp_queue)
        else:
            queue_path = os.path.join(path, self.cfg.wsl2win_dir, self.cfg.wsl2win_queue)

        file_path = self.cfg.change_path(file_path)
        if kwargs is None:
            kwargs = {}
        kwargs["file_path"] = file_path
        row = ": ".join([command, json.dumps(kwargs)])

        with open(queue_path, "r") as queue:
            if row in queue.read():
                return

        with open(queue_path, "a") as queue:
            queue.write(row)
            queue.write("\n")
