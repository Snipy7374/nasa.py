from __future__ import annotations
from typing import TypedDict
from datetime import datetime

import attrs

from ..asset import AsyncAsset, SyncAsset


__all__: tuple[str, ...] = (
    "RawAstronomyPicture",
    "AstronomyPicture",
)


class RawAstronomyPicture(TypedDict):
    copyright: str | None
    date: str
    explanation: str
    hdurl: str | None
    media_type: str
    service_version: str
    title: str
    url: str


def convert_to_date(string) -> datetime:
    return datetime.strptime(string, "%Y-%m-%d")


@attrs.define(kw_only=True, repr=True, eq=True)
class AstronomyPicture:
    copyright: str | None
    date: str = attrs.field(converter=convert_to_date)
    explanation: str
    hdurl: str | None
    media_type: str | None
    service_version: str
    title: str
    url: str
    image: SyncAsset | AsyncAsset 
    # i feel like this could be typed in a better way 
    # (if not we could need another class just for async responses)