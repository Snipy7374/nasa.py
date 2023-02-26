from __future__ import annotations
from typing import TYPE_CHECKING, overload

from requests import Response

if TYPE_CHECKING:
    from aiohttp import ClientResponse


class NasaException(Exception):
    pass


class HTTPException(NasaException):
    @overload
    def __init__(self, response: Response) -> None:
        ...
    
    @overload
    def __init__(self, response: ClientResponse, reason: str) -> None:
        ...

    def __init__(self, response: Response | ClientResponse, reason: str | None = None) -> None:
        self.code = (
            response.status_code if isinstance(response, Response)
            else response.status
        )
        try:
            self.message = reason
            if reason is None:
                response_: dict[str, str] = response.json()  # type: ignore
                self.message = response_["msg"] 
        except:
            if reason is None:
                self.message = response.text

        super().__init__("[{}] {}".format(
            self.code, (
                    self.message if isinstance(self.message, str)
                    else self.message["msg"]  # type: ignore
                )
            )
        )