import os
from watchdog.events import FileSystemEventHandler

def get_ext(filename):
    return os.path.splitext(filename)[-1].lower()


class ChangeHandler(FileSystemEventHandler):

    def __init__(self, *args, **kwargs):
        self.indexer = kwargs.pop('indexer')
        super(FileSystemEventHandler, self).__init__()

    def on_any_event(self, event):
        if event.is_directory:
            self._on_dir(event)
            return

        self.indexer.index_file(event.src_path)

    def _on_dir(self, event):
	pass

