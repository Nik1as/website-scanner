import asyncio
import json
import random
from urllib.parse import urljoin

import aiohttp

from utils import unique_not_none
from vulns import Vuln

with open("data/payloads/ssti.json") as f:
    PAYLOADS = json.load(f)


class SST(Vuln):

    async def check_ssti(self, session: aiohttp.ClientSession, args, method, path, params, param, payload, num):
        try:
            params_kwargs = {"params": params} if method == "get" else {"data": params}

            async with session.request(method, urljoin(args.url, path), **params_kwargs) as response:
                text = await response.text()
                if str(num * num) in text:
                    return f"SSTI: {method.upper()} {path} with parameter {param} and payload {payload}"
        except:
            pass

    async def run(self, session: aiohttp.ClientSession, args, dirs):
        num = random.randint(1_000, 100_000)
        payloads = [p.replace("x", str(num)) for p in PAYLOADS]

        tasks = []
        for method, path, params, param, payload in self.get_requests(dirs, payloads):
            tasks.append(self.check_ssti(session, args, method, path, params, param, payload, num))

        results = await asyncio.gather(*tasks)
        return unique_not_none(results)
