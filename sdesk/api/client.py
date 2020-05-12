from datetime import datetime as dt
from functools import wraps
from requests_toolbelt import sessions

from .auth import _SdeskAuth
from .resources import Notebook, Entry, File


class SdeskClientAutheticationError(Exception):
    """ Raised on authentication errors. """


class BaseUrlSession(sessions.BaseUrlSession):
    """
    Change sessions.BaseUrlSession default behavior.

    :meta private:
    """

    def create_url(self, url):
        if url.startswith("/"):
            url = url[1:]
        return super(BaseUrlSession, self).create_url(url)


class SdeskClient:
    def __init__(self, sdesk_host, schema="https", verify=False, disable_warning=False):
        """ Science Desk Client class

        The client will aims to be a implement several functions to make it easier to
        interact with Science Desk API.

        :param sdesk_host: ScienceDesk host name (e.g sciencedesk.mydomain.com)
        :type sdesk_host: str
        :param schema: URL Schema, defaults to "https"
        :type schema: str, optional
        :param verify: Verify SSL certificate, defaults to False
        :type verify: bool, optional
        :param disable_warning: Disable Insegure Request Warning, defaults to False
        :type disable_warning: bool, optional
        """
        if disable_warning:
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.http = BaseUrlSession(base_url=f"{schema}://{sdesk_host}/api/")
        self.http.hooks["response"] = [
            lambda response, *args, **kwargs: response.raise_for_status()
        ]
        self.http.verify = verify

    def auth_required(func):  # pylint: disable=no-self-argument
        @wraps(func)
        def wrap(*args, **kwargs):
            if not isinstance(args[0].http.auth, _SdeskAuth):
                raise SdeskClientAutheticationError(
                    "SdeskClient is not authenticated. Check the SdeskClient.authenticate method."
                )
            return func(*args, **kwargs)  # pylint: disable=not-callable

        return wrap

    def authenticate(self, username, password):
        """ Authenticate the client

        :param username: Username
        :type username: str
        :param password: Password
        :type password: str
        """
        response = self.http.post(
            "/token/", data=dict(username=username, password=password)
        )
        token = response.json().get("token")
        self.http.auth = _SdeskAuth(token)

    @auth_required
    def list_notebooks(self, limit=9999, offset=0):
        """ List SDesk Notebooks

        :param limit: Results Limit, defaults to 9999
        :type limit: int, optional
        :param offset: Results Offset, defaults to 0
        :type offset: int, optional

        :rtype: :class:`.Notebook` list

        """
        # TODO: Does SDesk API have a GET path to list notebooks?
        resp = self.http.post(
            f"/notebooks/diff/?limit={limit}&offset={offset}",
            json={"diff": [], "filter": {}, "fullData": False},
        )
        return [Notebook(n) for n in resp.json()["list"]]

    @auth_required
    def get_notebook(self, id):
        """ Get a Notebook by its ID

        :param id: Notebook id
        :type id: int

        :rtype: Notebook
        """
        resp = self.http.get(f"/notebooks/{id}/")
        return Notebook(resp.json())

    @auth_required
    def list_entries(self, notebook_id, limit=9999, offset=0):
        """ List Notebook's Entries

        :param notebook_id: Notebook id
        :type notebook_id: int
        :param limit: Results Limit, defaults to 9999
        :type limit: int, optional
        :param offset: Results Offset, defaults to 0
        :type offset: int, optional

        :rtype: :class:`.Entry` list
        """
        # TODO: Does SDesk API have a GET path to list entries?
        resp = self.http.post(
            f"/entries/diff/?limit={limit}&offset={offset}",
            json={"diff": [], "filter": {"labbookFK": "17"}, "fullData": False},
        )
        return [Entry(n) for n in resp.json()["list"]]

    @auth_required
    def list_files(self, limit=9999, offset=0):
        """ List Files

        :param limit: Results Limit, defaults to 9999
        :type limit: int, optional
        :param offset: Results Offset, defaults to 0
        :type offset: int, optional

        :rtype: :class:`.File` list
        """
        # TODO: Does SDesk API have a GET path to list files?
        resp = self.http.post(
            f"/notebooks/upldfiles/diff/?limit={limit}&offset={offset}",
            json={
                "diff": [],
                "filter": {"is_workspace": False, "owner__isnull": False},
                "fullData": False,
            },
        )
        return [File(n) for n in resp.json()["list"]]

    @auth_required
    def list_entry_files(self, entry, limit=9999, offset=0):
        """ List Files

        :param entry: Entry Id
        :type entry: int
        :param limit: Results Limit, defaults to 9999
        :type limit: int, optional
        :param offset: Results Offset, defaults to 0
        :type offset: int, optional

        :rtype: :class:`.File` list
        """
        # TODO: Does SDesk API have a GET path to list entry files?
        resp = self.http.post(
            f"/notebooks/upldfiles/diff/?limit={limit}&offset={offset}",
            json={
                "diff": [],
                "filter": {
                    "entryFK": entry,
                    "is_workspace": False,
                    "owner__isnull": False,
                },
                "fullData": False,
            },
        )
        return [File(n) for n in resp.json()["list"]]

    @auth_required
    def create_entry(
        self,
        notebook_id,
        description,
        title,
        datetime=None,
        submited=True,
        saved=True,
        task_id=None,
        sample_id=None,
    ):
        """ Create a new entry on a Notebook

        :param notebook_id: Notebook Id
        :type notebook_id: int
        :param description: Description
        :type description: str
        :param title: Title
        :type title: str
        :param datetime: Entry's datetime, defaults to now()
        :type datetime: datetime, optional
        :param submited: defaults to True
        :type submited: bool, optional
        :param saved: defaults to True
        :type saved: bool, optional
        :param task_id: defaults to None
        :type task_id: int, optional
        :param sample_id: defaults to None
        :type sample_id: int, optional

        :rtype: Entry
        """
        isodt = datetime.isoformat() if datetime else dt.now().isoformat()
        payload = dict(
            datetime=isodt,
            title=title,
            description=description,
            saved=saved,
            submitted=submited,
            sampleFK=sample_id,
            labbookFK=notebook_id,
            taskFK=task_id,
        )
        resp = self.http.post("/notebooks/entries/", json=payload)
        return Entry(resp.json()["instance"])

    @auth_required
    def upload_file(self, notebook_id, entry_code, file_path):
        """ Upload a file to a Notebook's Entry

        :param notebook_id: Notebook Id
        :type notebook_id: int
        :param entry_code: Entry Code
        :type entry_code: int
        :param file_path: Path to the file to be uploaded
        :type file_path: str

        :rtype: File
        """
        resp = self.http.post(
            f"/notebooks/{notebook_id}/entries/{entry_code}/upldfiles/",
            files={"file": open(file_path, "rb")},
        )
        return File(resp.json()["instances"][0])

    @auth_required
    def get_file_info(self, file_id):
        """Get a File by its Id

        :param file_id: File Id
        :type file_id: int

        :rtype: File
        """
        resp = self.http.get(f"/notebooks/upldfiles/{file_id}/")
        return File(resp.json())
