import os
import subprocess

from watchdog.events import FileSystemEventHandler

from ...callback import CallbackData
from ...config import Config


class StatusHandler(FileSystemEventHandler):

    def __init__(self, queue):
        super(StatusHandler, self).__init__()

        self.cfg = Config()
        self.queue = queue

    @property
    def track_folders(self):
        return list(self.cfg.projects.values())

    def on_modified(self, event):
        for path in self.track_folders:
            file_track = os.path.join(path, self.cfg.status_file)

            if not event.is_directory and event.src_path == file_track:
                command = [self.cfg.notepad_path, file_track]
                subprocess.call(command, cwd=path, stdout=None, shell=False)

                data = CallbackData(
                    event_handler="status",
                    event_type="modified",
                    value=file_track
                )
                self.queue.put(data)
                break
