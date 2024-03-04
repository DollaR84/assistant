from watchdog.observers import Observer

from .handlers import QueueHandler


class Watcher(Observer):

    def __init__(self, queue):
        super().__init__()

        self.queue = queue

        self.handlers = [QueueHandler]

        self.init_handlers()
        self.start()

    def init_handlers(self):
        for handler_cls in self.handlers:
            handler = handler_cls(self.queue)
            for track_folder in handler.track_folders:
                self.schedule(handler, path=track_folder, recursive=False)
