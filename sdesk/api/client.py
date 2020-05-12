from datetime import datetime as dt
from requests_toolbelt import sessions

from .auth import SdeskAuth
from .resources import Notebook, Entry, File


class SdeskClientAutheticationError(Exception):
    """ Raised on authentication errors. """


class BaseUrlSession(sessions.BaseUrlSession):
    def create_url(self, url):
        """ Change sessions.BaseUrlSession default behavior. """
        if url.startswith("/"):
            url = url[1:]
        return super(BaseUrlSession, self).create_url(url)


class SdeskClient:
    def __init__(self, sdesk_host, schema="https", verify=False, disable_warning=False):
        if disable_warning:
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.http = BaseUrlSession(base_url=f"{schema}://{sdesk_host}/api/")
        self.http.hooks["response"] = [
            lambda response, *args, **kwargs: response.raise_for_status()
        ]
        self.http.verify = verify

    def auth_required(func):  # pylint: disable=no-self-argument
        def wrap(*args, **kwargs):
            if not isinstance(args[0].http.auth, SdeskAuth):
                raise SdeskClientAutheticationError(
                    "SdeskClient is not authenticated. Check the SdeskClient.authenticate method."
                )
            return func(*args, **kwargs)  # pylint: disable=not-callable

        return wrap

    def authenticate(self, username, password):
        response = self.http.post(
            "/token/", data=dict(username=username, password=password)
        )
        token = response.json().get("token")
        self.http.auth = SdeskAuth(token)

    @auth_required
    def list_notebooks(self, limit=9999, offset=0):
        # TODO: Does SDesk API have a GET path to list notebooks?
        resp = self.http.post(
            f"/notebooks/diff/?limit={limit}&offset={offset}",
            json={"diff": [], "filter": {}, "fullData": False},
        )
        return [Notebook(n) for n in resp.json()["list"]]

    @auth_required
    def get_notebook(self, id):
        resp = self.http.get(f"/notebooks/{id}/")
        return Notebook(resp.json())

    @auth_required
    def list_entries(self, notebook_id, limit=9999, offset=0):
        # TODO: Does SDesk API have a GET path to list entries?
        resp = self.http.post(
            f"/entries/diff/?limit={limit}&offset={offset}",
            json={"diff": [], "filter": {"labbookFK": "17"}, "fullData": False},
        )
        return [Entry(n) for n in resp.json()["list"]]

    @auth_required
    def list_files(self, limit=9999, offset=0):
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
        resp = self.http.post(
            f"/notebooks/{notebook_id}/entries/{entry_code}/upldfiles/",
            files={"file": open(file_path, "rb")},
        )
        return File(resp.json()["instances"][0])

    @auth_required
    def get_file_info(self, file_id):
        resp = self.http.get(f"/notebooks/upldfiles/{file_id}/")
        return File(resp.json())
