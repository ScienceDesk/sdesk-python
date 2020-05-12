import os
import sys
import requests

__version__ = "0.2.2"


def check_published(uri, extension=".tar.gz"):
    url = os.path.join(uri, "sdesk", "sdesk-" + __version__ + extension)
    sys.stdout.write(str(requests.head(url).ok))


def published():
    if len(sys.argv) <= 1:
        sys.exit(1)

    uri, extension = sys.argv[1:3] if len(sys.argv) > 2 else [sys.argv[1], ".tar.gz"]
    check_published(uri, extension)
