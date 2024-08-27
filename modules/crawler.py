import asyncio
import re
from collections import defaultdict
from urllib.parse import urlparse, parse_qs, urljoin

import aiohttp
from bs4 import BeautifulSoup

from modules import Module
from utils import parse_form

HTML_COMMENT_REGEX = re.compile(r"<!--(.*?)-->", re.DOTALL)
EMAIL_REGEX = re.compile(r"\S+@\S+\.\S+")
HTTP_URL_REGEX = re.compile(r"https?://([a-zA-Z0-9.-]+)")
MAX_DEPTH = 1


class Directory:

    def __init__(self, directory: str):
        self.directory = directory
        self.url_parameters = defaultdict(set)
        self.post_parameters = defaultdict(set)

    def json(self):
        result = dict()
        if self.url_parameters:
            result["url_parameters"] = {k: list(v) for k, v in self.url_parameters.items()}
        if self.post_parameters:
            result["post_parameters"] = {k: list(v) for k, v in self.post_parameters.items()}
        return result


class Crawler(Module):

    def __init__(self):
        super().__init__("crawler")

    async def run(self, session: aiohttp.ClientSession, base_url: str):
        directories = dict()
        emails = set()
        comments = set()

        async def crawl(curr_url: str, depth: int):
            if depth > MAX_DEPTH:
                return

            try:
                async with session.get(curr_url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    for match in EMAIL_REGEX.findall(html):
                        emails.add(match)
                    for match in HTML_COMMENT_REGEX.findall(html):
                        comments.add(match.strip())
                    for form in soup.find_all("form"):
                        method, action, args = parse_form(form)

                        if action not in directories:
                            directory = Directory(action)
                            directories[action] = directory
                        else:
                            directory = directories[action]

                        for name, value in args.items():
                            if method.casefold() == "post":
                                directory.post_parameters[name].add(value)
                            elif method.casefold() == "get":
                                directory.url_parameters[name].add(value)

                    urls = set()
                    curr_domain = urlparse(curr_url).netloc
                    for link in soup.find_all("a"):
                        href = link.get("href")
                        if href is None:
                            continue

                        new_url = href
                        if re.match(HTTP_URL_REGEX, href):
                            href_domain = urlparse(href).netloc
                            if href_domain != curr_domain:
                                continue
                        else:
                            new_url = urljoin(curr_url, href)

                        parsed = urlparse(new_url)
                        if parsed.path not in directories:
                            directory = Directory(parsed.path)
                            directories[parsed.path] = directory
                            urls.add(new_url)
                        else:
                            directory = directories[parsed.path]

                        for key, values in parse_qs(parsed.query).items():
                            if any(v not in directory.url_parameters[key] for v in values):
                                urls.add(new_url)
                            directory.url_parameters[key].update(values)

                    await asyncio.gather(*[crawl(new_url, depth + 1) for new_url in urls])
            except (aiohttp.ClientError, asyncio.TimeoutError):
                pass

        parsed = urlparse(base_url)
        directory = Directory(parsed.path)
        directories[parsed.path] = directory

        await crawl(base_url, 1)

        return {
            "directories": {d.directory: d.json() for d in directories.values()},
            "emails": list(emails),
            "comments": list(comments)
        }
