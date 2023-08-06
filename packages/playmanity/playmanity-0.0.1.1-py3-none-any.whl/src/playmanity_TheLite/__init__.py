import asyncio
try:
    from typing import NamedTuple, Literal
except ImportError:
    from typing_extensions import NamedTuple, Literal
import requests
from . import accounts

__title__ = 'playmanity'
__author__ = 'TheLite'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022-present TheLite & BetterPlaymanity'
__version__ = '0.1.0a'


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(major=0, minor=0, micro=1, releaselevel='alpha', serial=0)


class get():
    def __init__(self):
            pass

    def getBotProfile(bot:accounts.Bot):
        async def get():
            Head = {"Authorization": bot.__dict__["token"]["token"]}
            res = requests.get("https://api.playmanity.com/user/small-profile", headers=Head)
            if res.status_code == 200:
                return res.json()
            else:
                return res.status_code
        return asyncio.run(get())
    
    def getProfile(user:str):
        async def get():
            res = requests.get(f"https://api.playmanity.com/user/{user}/profile")
            if res.status_code == 200:
                return res.json()
            else:
                return res.status_code
        return asyncio.run(get())