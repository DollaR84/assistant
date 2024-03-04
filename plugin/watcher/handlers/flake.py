import os
import subprocess

from watchdog.events import FileSystemEventHandler

from ...config import Config


class FlakeHandler(FileSystemEventHandler):

    def __init__(self, queue):
        super(FlakeHandler, self).__init__()

        self.cfg = Config()
        self.queue = queue

    @property
    def track_folders(self):
        return list(self.cfg.projects.values())

    def on_modified(self, event):
        for path in self.track_folders:
            file_track = os.path.join(path, self.cfg.flake_file)

            if not event.is_directory and event.src_path == file_track:
                command = [self.cfg.notepad_path, file_track]
                subprocess.call(command, cwd=path, stdout=None, shell=False)
                break
