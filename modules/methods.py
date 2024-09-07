import aiohttp

from modules import Module

METHODS = ["get", "post", "put", "delete", "head", "options", "patch"]


class Methods(Module):

    def __init__(self):
        super().__init__("methods")

    async def run(self, session: aiohttp.ClientSession, args):
        result = []
        for method in METHODS:
            async with session.request(method, args.url) as response:
                if response.status not in (405, 501):
                    result.append(method)

        return result
