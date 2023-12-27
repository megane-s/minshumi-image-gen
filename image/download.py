import hashlib
import mimetypes
import os
from os import path
from typing import cast
from urllib.parse import urlparse

import requests
from requests import Response

from util.env import get_env

tmp_dir = path.join(get_env("TMP_DIR"), "_remote_images")

def get_local_path(url:str):
    sha256 = hashlib.sha256()
    sha256.update(url.encode())
    url_hash = str(sha256.hexdigest())
    response :Response = requests.get(url)
    content_type = response.headers.get('Content-Type')
    if content_type is None:
        return None
    ext = mimetypes.guess_extension(cast(str, content_type), strict=False)
    if ext is None:
        return None
    output_path = path.join(tmp_dir, f"{url_hash}{ext}")
    if not path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    with open(output_path, "wb") as file:
        file.write(cast(bytes, response.content))
    return output_path
