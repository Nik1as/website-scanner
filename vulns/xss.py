import asyncio
import json
from urllib.parse import urljoin

import aiohttp

from utils import unique_not_none
from vulns import Vuln

with open("data/payloads/xss.json") as f:
    PAYLOADS = json.load(f)


class XSS(Vuln):

    async def check_xss(self, session: aiohttp.ClientSession, args, method, path, params, param, payload):
        try:
            params_kwargs = {"params": params} if method == "get" else {"data": params}

            async with session.request(method, urljoin(args.url, path), **params_kwargs) as response:
                text = await response.text()
                if payload in text:
                    return f"XSS: {method.upper()} {path} with parameter {param}"
        except:
            pass

    async def run(self, session: aiohttp.ClientSession, args, dirs):
        tasks = []
        for method, path, params, param, payload in self.get_requests(dirs, PAYLOADS):
            tasks.append(self.check_xss(session, args, method, path, params, param, payload))

        results = await asyncio.gather(*tasks)
        return unique_not_none(results)
