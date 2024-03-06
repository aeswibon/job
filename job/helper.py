import base64
import hashlib
import os
import re

from django.conf import settings
from requests_oauthlib import OAuth2Session

from job.constants import SCOPES


def generate_code_verifier() -> str:
    tmp = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
    return re.sub("[^a-zA-Z0-9]+", "", tmp)


def generate_code_challenge(code_verifier: str) -> str:
    tmp = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    tmp = base64.urlsafe_b64encode(tmp).decode("utf-8")
    return tmp.replace("=", "")


def make_token():
    return OAuth2Session(
        settings.CLIENT_ID, redirect_uri=settings.REDIRECT_URI, scope=SCOPES
    )
