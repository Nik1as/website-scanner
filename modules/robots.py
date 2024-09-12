import json
from urllib.parse import urljoin

import aiohttp

from modules import Module
from utils import get_req_kwargs


class Robots(Module):

    def __init__(self):
        super().__init__("robots.txt")

    async def run(self, session: aiohttp.ClientSession, args):
        async with session.get(urljoin(args.url, "/robots.txt"), **get_req_kwargs(args)) as response:
            if response.status == 200:
                text = await response.text()
                text = [line for line in text.splitlines() if line.strip()]
                return json.dumps(text)
