import os

from callback import CallbackData
from config import Config

from watchdog.events import FileSystemEventHandler


class QueueHandler(FileSystemEventHandler):

    def __init__(self, queue):
        super().__init__()

        self.cfg = Config()
        self.queue = queue

    @property
    def track_folders(self) -> list[str]:
        return [os.path.join(path, self.cfg.wsl2win_dir) for path in self.cfg.projects.values()]

    def on_modified(self, event):
        for name, path in self.cfg.projects.items():
            file_track = os.path.join(path, self.cfg.wsl2win_dir, self.cfg.wsl2win_queue)

            if not event.is_directory and event.src_path == file_track:
                data = CallbackData(
                    event_handler="queue",
                    event_type="modified",
                    value=name,
                )
                self.queue.put(data)
                break
