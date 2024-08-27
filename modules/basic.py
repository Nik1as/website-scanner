import aiohttp
from bs4 import BeautifulSoup

from modules import Module


class Basic(Module):

    def __init__(self):
        super().__init__("basic")

    async def run(self, session: aiohttp.ClientSession, base_url: str):
        async with session.get(base_url, allow_redirects=True) as response:
            result = dict()

            content = await response.text()
            soup = BeautifulSoup(content, "html.parser")
            if soup.title:
                result["title"] = soup.title.string

            generator_tag = soup.find("meta", attrs={"name": "generator"})
            if generator_tag and "content" in generator_tag.attrs:
                result["generator"] = generator_tag["content"]

            if response.history:
                result["redirect"] = str(response.url)

            return result
