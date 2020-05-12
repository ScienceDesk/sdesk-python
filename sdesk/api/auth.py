from requests import auth


class _SdeskAuth(auth.AuthBase):
    """Attaches HTTP Token Authentication to the given Request object."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Token " + self.token
        return r
