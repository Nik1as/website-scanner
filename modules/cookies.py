import aiohttp

from modules import Module


class CookieFlag(Module):

    def __init__(self):
        super().__init__("cookies")

    async def run(self, session: aiohttp.ClientSession, args):
        async with session.get(args.url) as response:
            result = dict()
            for cookie in response.cookies.values():
                if not cookie["secure"] or not cookie["httponly"]:
                    result[cookie.key] = {
                        "name": cookie.key,
                        "value": cookie.value,
                        "secure": cookie["secure"],
                        "httponly": cookie["httponly"],
                    }

            return result
