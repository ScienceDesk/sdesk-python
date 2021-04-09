from copy import deepcopy


class ResourceBase:
    def __init__(self, data):
        self._data = data

    def _get(self, key):
        return self._data.get(key)

    @property
    def id(self):
        return self._get("id")

    @property
    def full_data(self):
        return deepcopy(self._data)


class User(ResourceBase):
    @property
    def first_name(self):
        return self._get("first_name")

    @property
    def last_name(self):
        return self._get("last_name")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Notebook(ResourceBase):
    @property
    def id(self):
        return self._get("id")

    @property
    def description(self):
        return self._get("description")

    @property
    def title(self):
        return self._get("title")

    @property
    def owner(self):
        return User(self._get("owner") or dict())


class Entry(ResourceBase):
    @property
    def author(self):
        return User(self._get("author"))

    @property
    def code(self):
        return self._get("entrycode")

    @property
    def title(self):
        return self._get("title")

    @property
    def files(self):
        # "datafiles": [7, 5, 6, 1, 4, 3, 2],
        return self._get("datafiles")


class File(ResourceBase):
    @property
    def name(self):
        return self._get("filename")

    @property
    def type(self):
        return self._get("filetype")

    @property
    def owner(self):
        return User(self._get("owner") or dict())

    @property
    def uploader(self):
        return User(self._get("uploadedby") or dict())

    @property
    def user(self):
        return User(self._get("user") or dict())

    @property
    def labbookFK(self):
        return self._get("labbookFK")

    @property
    def url(self):
        return self._get("urldatafile")
