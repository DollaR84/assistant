import os
import subprocess

from watchdog.events import FileSystemEventHandler

from ...config import Config


class ErrorsHandler(FileSystemEventHandler):

    def __init__(self, queue):
        super(ErrorsHandler, self).__init__()

        self.cfg = Config()
        self.queue = queue

    @property
    def track_folders(self):
        return self.cfg.project_logs_folders

    def on_modified(self, event):
        for path in self.track_folders:
            file_track = os.path.join(path, self.cfg.get_project_logs_file_name(path))

            if not event.is_directory and event.src_path == file_track:
                command = [self.cfg.notepad_path, file_track, "-n10000"]
                subprocess.call(command, cwd=path, stdout=None, shell=False)
                break
