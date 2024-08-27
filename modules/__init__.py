import os
import traceback
from abc import ABC, abstractmethod
from importlib import util

import aiohttp


class Module(ABC):
    modules = []

    def __init__(self, name: str):
        self.name = name

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.modules.append(cls)

    async def start(self, session: aiohttp.ClientSession, base_url: str):
        return self.name, await self.run(session, base_url)

    @abstractmethod
    async def run(self, session: aiohttp.ClientSession, base_url: str):
        pass


def load_module(path):
    name = os.path.split(path)[-1]
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)

for fname in os.listdir(dirpath):
    if not fname.startswith('.') and \
            not fname.startswith('__') and fname.endswith('.py'):
        try:
            load_module(os.path.join(dirpath, fname))
        except:
            traceback.print_exc()
