from enum import Enum

__all__: tuple[str, ...] = (
    "Endpoints",
)

class Endpoints(str, Enum):
    APOD = "/planetary/apod"