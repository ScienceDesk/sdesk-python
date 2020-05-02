import pytest

import requests
import toml

from sdesk import __version__, api


API_URL = "http://localhost:8000/api"


def test_version():
    assert __version__ == toml.load("pyproject.toml")["tool"]["poetry"]["version"]


@pytest.mark.skip(reason="External dependency")
def test_auth():
    def get_token(s, user, password):
        creds = {"username": user, "password": password}

        r = s.post(API_URL + "/token/", data=creds)
        return r.json().get("token")

    s = requests.Session()
    token = get_token(s, "the-user", "secret!")
    s.auth = api.SdeskAuth(token)
