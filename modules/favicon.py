import hashlib
import json
from urllib.parse import urljoin

import aiohttp

from modules import Module

with open("data/favicon-database.json") as f:
    DATABASE = json.load(f)


class Favicon(Module):

    def __init__(self):
        super().__init__("favicon")

    async def run(self, session: aiohttp.ClientSession, base_url: str):
        async with session.get(urljoin(base_url, "favicon.ico")) as response:
            if response.status == 200:
                favicon_hash = hashlib.md5(await response.read()).hexdigest()

                for entry in DATABASE:
                    if entry["hash"] == favicon_hash:
                        return entry["name"]
                return favicon_hash
