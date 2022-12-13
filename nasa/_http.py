from __future__ import annotations

import requests
import sys

from typing import ClassVar

from ._types import RawAstronomyPicture

class Route:
    BASE_API_URL: ClassVar[str] = "https://api.nasa.gov"

    def __init__(self, method: str, path: str) -> None:
        self.path = path
        self.method = method
        self.url = self.BASE_API_URL + self.path


class HTTPClient:
    def __init__(self, token: str | None = None) -> None:
        self.__token = token
        self._user_agent = f"Nasa.py 0.0.1a (GitHub here) Python/{sys.version_info[0]}.{sys.version_info[1]} requests/{requests.__version__}"

    def request(
        self,
        *,
        route: Route,
        params: dict[str, str]
    ) -> RawAstronomyPicture:
        url = route.url
        headers: dict[str, str] = {
            "User-Agent": self._user_agent,
        }
        if not self.__token:
            raise # add token exception here

        if params and self.__token:
            params["api_key"] = self.__token

        response = requests.request(method=route.method, headers=headers, params=params, url=url).json()
        if "error" in response.keys():
            print(response)
        return RawAstronomyPicture(**(response))
        

