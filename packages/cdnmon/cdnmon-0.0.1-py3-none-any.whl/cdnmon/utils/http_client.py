import datetime
import hashlib
import os
import requests

from cdnmon.utils.logging import logger
from cdnmon.utils.misc import get_project_root
from cdnmon.utils.storage import save_to_minio


def http_cached_requests(url, cache_folder, method="GET", params=None, headers=None, cookies=None, session=None):
    if params is None:
        params = {}
    if headers is None:
        headers = {}
    if cookies is None:
        cookies = {}
    request = requests.Request(method=method, url=url, params=params, headers=headers, cookies=cookies)
    prepped = request.prepare()
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    url_md5 = hashlib.md5(prepped.url.encode("utf-8")).hexdigest()
    relative_filepath = f"{today}/{cache_folder}/{url_md5}.html"
    cache_filepath = f"{get_project_root()}/.cache/{relative_filepath}"
    if os.path.exists(cache_filepath):
        logger.info(f"[HIT] {cache_filepath}")
        content = open(cache_filepath, "rb").read()
    else:
        if session is None:
            session = requests.Session()
        response = session.send(prepped)
        logger.info(f"[MISS] {response.url}")
        content = response.content
        if response.status_code == 200:
            try:
                os.makedirs(os.path.dirname(cache_filepath))
            except Exception as e:
                logger.error(repr(e))
            with open(cache_filepath, "wb") as f:
                f.write(content)
            save_to_minio(cache_filepath, relative_filepath)
        else:
            logger.warn(f"[{response.status_code}] ({len(response.content)} Bytes) {url} ")
    return content
