from sdesk import __version__, api
import requests


API_URL = "http://localhost:8000/api"


def test_version():
    assert __version__ == "0.1.0"


def get_token(s, user, password):
    creds = {"username": user, "password": password}

    r = s.post(API_URL + "/token/", data=creds)
    return r.json().get("token")


def test_auth():
    s = requests.Session()
    token = get_token(s, "the-user", "secret!")
    s.auth = api.SdeskAuth(token)
