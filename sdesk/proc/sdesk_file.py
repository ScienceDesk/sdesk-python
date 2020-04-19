import pathlib


class SdeskFile:

    def __init__(self, path, metadata={}):
        self._file_path = path
        self._metadata = metadata

    def name(self):
        return pathlib.Path(self._file_path).name

    def path(self):
        return self._file_path

    def update_metadata(self, metadata):
        self._metadata = metadata

    def metadata(self):
        return self._metadata
