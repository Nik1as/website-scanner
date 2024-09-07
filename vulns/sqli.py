import asyncio
import json
from urllib.parse import urljoin

import aiohttp

from utils import unique_not_none
from vulns import Vuln

with open("data/payloads/sqli.json") as f:
    PAYLOADS = json.load(f)


class SQLI(Vuln):

    async def check_error_based(self, session: aiohttp.ClientSession, args, method, path, params, param):
        try:
            params_kwargs = {"params": params} if method == "get" else {"data": params}

            async with session.request(method, urljoin(args.url, path), **params_kwargs) as response:
                text = await response.text()
                text = text.casefold()
                if any(msg in text for msg in PAYLOADS["error-based"]["messages"]):
                    return f"SQL-Injection (error-based): {method.upper()} {path} with parameter {param}"
        except:
            pass

    async def error_based(self, session: aiohttp.ClientSession, args, dirs):
        tasks = []
        for method, path, params, param, _ in self.get_requests(dirs, PAYLOADS["error-based"]["payloads"]):
            tasks.append(self.check_error_based(session, args, method, path, params, param))

        results = await asyncio.gather(*tasks)
        return unique_not_none(results)

    async def run(self, session: aiohttp.ClientSession, args, dirs):
        return await self.error_based(session, args, dirs)
