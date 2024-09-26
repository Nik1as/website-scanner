import hashlib
import json
import re
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup

from modules import Module
from regex import HTTP_URL_REGEX
from utils import get_req_kwargs

with open("data/favicon-database.json") as f:
    DATABASE = json.load(f)


class Favicon(Module):

    def __init__(self):
        super().__init__("favicon")

    async def run(self, session: aiohttp.ClientSession, args):
        favicon_url = None
        async with session.get(args.url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            icon_link = soup.find("link", rel="shortcut icon")
            if icon_link is not None:
                favicon_url = icon_link["href"]
                if not re.match(HTTP_URL_REGEX, favicon_url):
                    favicon_url = urljoin(args.url, favicon_url)

        favicon_url = favicon_url or urljoin(args.url, "favicon.ico")
        async with session.get(favicon_url, **get_req_kwargs(args)) as response:
            if response.status == 200:
                favicon_hash = hashlib.md5(await response.read()).hexdigest()

                for entry in DATABASE:
                    if entry["hash"] == favicon_hash:
                        return entry["name"]
                return favicon_hash
