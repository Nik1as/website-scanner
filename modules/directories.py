import asyncio
from urllib.parse import urljoin

import aiohttp

from modules import Module
from utils import get_req_kwargs

with open("data/directories.txt", "r") as f:
    DIRECTORIES = [line.strip() for line in f.readlines()]


class Directories(Module):

    def __init__(self):
        super().__init__("directories")

    async def check(self, session: aiohttp.ClientSession, base_url: str, directory: str, args):
        async with session.get(urljoin(base_url, f"/{directory}"), **get_req_kwargs(args)) as response:
            if response.status != 404:
                return f"/{directory}"

    async def run(self, session: aiohttp.ClientSession, args):
        results = await asyncio.gather(*[self.check(session, args.url, directory, args)
                                         for directory in DIRECTORIES
                                         if f"/{directory}" not in args.ignore])
        return [result for result in results if result is not None]
