import aiohttp

from modules import Module


class Methods(Module):

    def __init__(self):
        super().__init__("methods")

    async def run(self, session: aiohttp.ClientSession, base_url: str):
        methods = [("get", session.get), ("post", session.post), ("put", session.put), ("delete", session.delete), ("head", session.head),
                   ("options", session.options), ("patch", session.patch)]

        result = []
        for method, func in methods:
            async with func(base_url) as response:
                if response.status not in (405, 501):
                    result.append(method)

        return result
