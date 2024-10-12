import json
import random
import re
import string
from urllib.parse import urljoin

import aiohttp

from modules import Module

with open("data/404.json", "r") as f:
    DATABASE = json.load(f)


class NotFoundPage(Module):

    def __init__(self):
        super().__init__("not-found-page")

    async def run(self, session: aiohttp.ClientSession, args):
        path = "".join(random.choices(string.ascii_uppercase, k=16))
        url = urljoin(args.url, path)
        async with session.get(url) as response:
            text = await response.text()
            text = re.sub(r"\s+", "", text)
            for framework, fingerprint in DATABASE.items():
                if re.match(fingerprint, text, re.IGNORECASE | re.DOTALL):
                    return framework
