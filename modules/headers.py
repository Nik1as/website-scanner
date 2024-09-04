import aiohttp

from modules import Module

INTERESTING_HEADERS = ["Server", "X-Powered-By", "PHP", "X-Version", "X-Runtime", "X-AspNet-Version"]


class Headers(Module):

    def __init__(self):
        super().__init__("headers")

    async def run(self, session: aiohttp.ClientSession, args):
        async with session.get(args.url) as response:
            result = dict()
            for header in INTERESTING_HEADERS:
                if header in response.headers:
                    result[header] = response.headers.get(header)
            return result
