import aiohttp

from modules import Module
from utils import get_req_kwargs

METHODS = ["get", "post", "put", "delete", "head", "options", "patch"]


class Methods(Module):

    def __init__(self):
        super().__init__("methods")

    async def run(self, session: aiohttp.ClientSession, args):
        result = []
        for method in METHODS:
            try:
                async with session.request(method, args.url, **get_req_kwargs(args)) as response:
                    if response.status not in (405, 501):
                        result.append(method)
            except aiohttp.ServerDisconnectedError:
                pass

        return result
