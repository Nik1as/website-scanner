import json
from urllib.parse import urljoin

import aiohttp

from modules import Module


class Robots(Module):

    def __init__(self):
        super().__init__("robots.txt")

    async def run(self, session: aiohttp.ClientSession, base_url: str):
        async with session.get(urljoin(base_url, "/robots.txt")) as response:
            if response.status == 200:
                text = await response.text()
                text = [line for line in text.splitlines() if line.strip()]
                return json.dumps(text)
