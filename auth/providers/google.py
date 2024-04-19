from google_auth_oauthlib.flow import Flow
from flask import url_for
import pathlib
from json import loads

import os, sys

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev | remove in production 
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"]  = "1"

try:
    client_secret_config = loads(os.environ["GOOGLE_CLIENT_SECRET"])
    flow = Flow.from_client_config(
        client_config=client_secret_config,
        scopes="openid profile email"
    )
except:
    client_secrets_file = os.getcwd() +"/"+ os.environ["GOOGLE_CLIENT_SECRET"]

    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes="openid profile email"
    )
