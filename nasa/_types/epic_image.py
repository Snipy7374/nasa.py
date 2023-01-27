from __future__ import annotations
from typing import TypedDict

import attrs

from ..asset import AsyncAsset, SyncAsset

__all__: tuple[str, ...] = (
    "_EpicCoordinates",
    "RawEpicImage",
    "Coordinates",
    "EpicImage",
)


class _EpicCoordinates(TypedDict):
    lat: str
    lon: str
    centroid_coordinates: str
    dscovr_j2000_position: str
    lunar_j2000_position: str
    sun_j2000_position: str
    attitude_quaternions: str


class RawEpicImage(TypedDict):
    image: str
    date: str
    caption: str
    centroid_coordinates: str
    dscovr_j2000_position: str
    lunar_j2000_position: str
    sun_j2000_position: str
    attitude_quaternions: str
    coords: _EpicCoordinates


@attrs.define(kw_only=True, repr=True, eq=True)
class Coordinates:
    lat: str
    lon: str
    centroid_coordinates: str
    dscovr_j2000_position: str
    lunar_j2000_position: str
    sun_j2000_position: str
    attitude_quaternions: str


@attrs.define(kw_only=True, repr=True, eq=True)
class EpicImage:
    image_name: str
    image: SyncAsset | AsyncAsset | None = None
    date: str
    caption: str
    centroid_coordinates: str
    dscovr_j2000_position: str
    lunar_j2000_position: str
    sun_j2000_position: str
    attitude_quaternions: str
    coords: Coordinates