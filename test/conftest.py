import os

username = os.environ.get("BCO_USERNAME")
password = os.environ.get("BCO_PASSWORD")

if username is None or password is None:
    raise Exception(
        "Please define your BCO FTP username and password"
        " with the environment variables `BCO_USERNAME` and"
        " `BCO_PASSWORD`"
    )
