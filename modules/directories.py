import asyncio
from urllib.parse import urljoin

import aiohttp

from modules import Module

with open("data/directories.txt", "r") as f:
    DIRECTORIES = [line.strip() for line in f.readlines()]


class Directories(Module):

    def __init__(self):
        super().__init__("directories")

    async def check(self, session: aiohttp.ClientSession, base_url: str, directory: str):
        async with session.get(urljoin(base_url, f"/{directory.lstrip('/')}")) as response:
            if response.status != 404:
                return directory

    async def run(self, session: aiohttp.ClientSession, base_url: str):
        results = await asyncio.gather(*[self.check(session, base_url, directory) for directory in DIRECTORIES])
        return [result for result in results if result is not None]
