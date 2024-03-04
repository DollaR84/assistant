from watchdog.observers import Observer

from .handlers import handlers


class Watcher(Observer):

    def __init__(self, queue):
        super(Watcher, self).__init__()

        self.queue = queue

        self.init_handlers()
        self.start()

    def init_handlers(self):
        for handler_cls in handlers:
            handler = handler_cls(self.queue)
            for track_folder in handler.track_folders:
                self.schedule(handler, path=track_folder, recursive=False)
