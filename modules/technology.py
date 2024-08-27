import json
import re

import aiohttp

from modules import Module

with open("data/technologies.json", "r") as f:
    TECHNOLOGIES = json.load(f)
with open("data/categories.json", "r") as f:
    CATEGORIES = json.load(f)


def contains(v, regex):
    if isinstance(v, bytes):
        v = v.decode()
    return re.compile(re.split(r"\\;", regex)[0], re.IGNORECASE).search(v)


def contains_dict(d1, d2):
    for k2, v2 in d2.items():
        v1 = d1.get(k2)
        if v1:
            if not contains(v1, v2):
                return False
        else:
            return False
    return True


def get_categories(spec):
    return [CATEGORIES[str(c_id)]["name"] for c_id in spec["cats"]]


def add_app(techs, name, spec):
    for category in get_categories(spec):
        if category not in techs:
            techs[category] = []
        if name not in techs[category]:
            techs[category].append(name)
            implies = spec.get("implies", [])
            if not isinstance(implies, list):
                implies = [implies]
            for app_name in implies:
                add_app(techs, app_name, TECHNOLOGIES[name])


class Technology(Module):

    def __init__(self):
        super().__init__("technology")

    async def run(self, session: aiohttp.ClientSession, base_url: str):
        async with session.get(base_url) as response:
            headers = response.headers
            cookies = response.cookies
            html = await response.text()

            results = dict()
            for name, spec in TECHNOLOGIES.items():
                if "headers" in spec and contains_dict(headers, spec["headers"]):
                    add_app(results, name, spec)

                if "cookies" in spec and contains_dict(cookies, spec["cookies"]):
                    add_app(results, name, spec)

                patterns = spec.get("html", [])
                if not isinstance(patterns, list):
                    patterns = [patterns]
                for pattern in patterns:
                    if contains(html, pattern):
                        add_app(results, name, spec)
                        break

            return results
