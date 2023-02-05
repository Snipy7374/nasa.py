from typing import Any


class NasaException(Exception):
    pass


class HTTPException(NasaException):
    def __init__(self, response: dict[str, Any], message: str) -> None:
        self.response = response
        super().__init__()