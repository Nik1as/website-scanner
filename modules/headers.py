import aiohttp

from modules import Module
from utils import get_req_kwargs

INTERESTING_HEADERS = ["Server", "X-Powered-By", "PHP", "X-Version", "X-Runtime", "X-AspNet-Version"]


class Headers(Module):

    def __init__(self):
        super().__init__("headers")

    async def run(self, session: aiohttp.ClientSession, args):
        async with session.get(args.url, **get_req_kwargs(args)) as response:
            result = dict()
            for header in INTERESTING_HEADERS:
                if header in response.headers:
                    result[header] = response.headers.get(header)
            return result
