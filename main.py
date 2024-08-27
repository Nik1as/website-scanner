import argparse
import asyncio
import json

import aiohttp

from modules import Module


def parse_args():
    parser = argparse.ArgumentParser(description="Scan a website",
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
    parser.add_argument("-u", "--url", type=str, required=True, help="URL to scan")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output json file")
    parser.add_argument("-c", "--cookie", type=str, required=False, default="", help="Cookie")
    parser.add_argument("-t", "--timeout", type=int, required=False, default=60, help="Timeout")
    parser.add_argument("--user-agent", type=str, required=False, default="webscan", help="User Agent")

    return parser.parse_args()


async def main():
    args = parse_args()

    headers = dict()
    if args.cookie:
        headers["cookie"] = args.cookie
    if args.user_agent:
        headers["user-agent"] = args.user_agent

    async with aiohttp.ClientSession(headers=headers, timeout=aiohttp.ClientTimeout(args.timeout)) as session:
        tasks = [module().start(session, args.url) for module in Module.modules]
        results = await asyncio.gather(*tasks)

        output = dict()
        for name, result in results:
            if result:
                output[name] = result

        with open(args.output, "w") as outfile:
            json.dump(output, outfile, indent=2)


if __name__ == "__main__":
    asyncio.run(main())
