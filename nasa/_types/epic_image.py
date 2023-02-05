from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

import attrs

from ..asset import AsyncAsset, SyncAsset

if TYPE_CHECKING:
    from datetime import datetime

__all__: tuple[str, ...] = (
    "RawEpicImage",
    "SpatialCoordinates",
    "EarthLikeCoordinates",
    "AttitudeQuaternions",
    "Coordinates",
    "EpicImage",
)


class _RawSpatialCoordinates(TypedDict):
    """
    Attributes
    ----------
    x: :class:`float`
    y: :class:`float`
    z: :class:`float`
    """
    x: float
    y: float
    z: float


class _RawEarthLikeCoordinates(TypedDict):
    """
    Attributes
    ----------
    lat: :class:`float`
    lon: :class:`float`
    """
    lat: float
    lon: float


class _RawAttitudeQ(TypedDict):
    """
    Attributes
    ----------
    q0: :class:`float`
    q1: :class:`float`
    q2: :class:`float`
    q3: :class:`float`
    """
    q0: float
    q1: float
    q2: float
    q3: float


class _EpicCoordinates(TypedDict):
    """
    Attributes
    ----------
    centroid_coordinates: :class:`_RawEarthLikeCoordinates`
    dscovr_j2000_position: :class:`_RawSpatialCoordinates`
    lunar_j2000_position: :class:`_RawSpatialCoordinates`
    sun_j2000_position: :class:`_RawSpatialCoordinates`
    attitude_quaternions: :class:`_RawAttituedeQ`
    """
    centroid_coordinates: _RawEarthLikeCoordinates
    dscovr_j2000_position: _RawSpatialCoordinates
    lunar_j2000_position: _RawSpatialCoordinates
    sun_j2000_position: _RawSpatialCoordinates
    attitude_quaternions: _RawAttitudeQ


class RawEpicImage(TypedDict):
    """
    Attributes
    ----------
    identifier: :class:`str`
    image: :class:`str`
    date: :class:`str`
    caption: :class:`str`
    centroid_coordinates: :class:`_RawEarthLikeCoordinates`
    dscovr_j2000_position: :class:`_RawSpatialCoordinates`
    lunar_j2000_position: :class:`_RawSpatialCoordinates`
    sun_j2000_position: :class:`_RawSpatialCoordinates`
    attitude_quaternions: :class:`_RawAttituedeQ`
    coords: :class:`_EpicCoordinates`
    version: :class:`int`
    """
    identifier: str
    image: str
    date: datetime
    caption: str
    centroid_coordinates: _RawEarthLikeCoordinates
    dscovr_j2000_position: _RawSpatialCoordinates
    lunar_j2000_position: _RawSpatialCoordinates
    sun_j2000_position: _RawSpatialCoordinates
    attitude_quaternions: _RawAttitudeQ
    coords: _EpicCoordinates
    version: int


@attrs.define(kw_only=True, repr=True)
class SpatialCoordinates:
    """
    Attributes
    ----------
    x: :class:`float`
    y: :class:`float`
    z: :class:`float`
    """
    x: float
    y: float
    z: float


@attrs.define(kw_only=True, repr=True)
class EarthLikeCoordinates:
    """
    Attributes
    ----------
    lat: :class:`float`
    lon: :class:`float`
    """
    lat: float
    lon: float


@attrs.define(kw_only=True, repr=True)
class AttitudeQuaternions:
    """
    Attributes
    ----------
    q0: :class:`float`
    q1: :class:`float`
    q2: :class:`float`
    q3: :class:`float`
    """
    q0: float
    q1: float
    q2: float
    q3: float


@attrs.define(kw_only=True, repr=True, eq=True)
class Coordinates:
    """
    Attributes
    ----------
    centroid_coordinates: :class:`EarthLikeCoordinates`
    dscovr_j2000_position: :class:`SpatialCoordinates`
    lunar_j2000_position: :class:`SpatialCoordinates`
    sun_j2000_position: :class:`SpatialCoordinates`
    attitude_quaternions: :class:`AttitudeQuaternions` 
    """
    centroid_coordinates: EarthLikeCoordinates
    dscovr_j2000_position: SpatialCoordinates
    lunar_j2000_position: SpatialCoordinates
    sun_j2000_position: SpatialCoordinates
    attitude_quaternions: AttitudeQuaternions


@attrs.define(kw_only=True, repr=True, eq=True)
class EpicImage:
    """Represents an epic image object returned by the NASA Api.

    .. versionadded:: 0.0.1

    Attributes
    ----------
    identifier: :class:`str`
    image_name: :class:`str`
    image: Optional[Union[:class:`SyncAsset`, :class:`AsyncAsset`]]
    date: :class:`datetime.datetime`
    caption: :class:`str`
    centroid_coordinates: :class:`EarthLikeCoordinates`
    dscovr_j2000_position: :class:`SpatialCoordinates`
    lunar_j2000_position: :class:`SpatialCoordinates`
    sun_j2000_position: :class:`SpatialCoordinates`
    attitude_quaternions: :class:`AttitudeQuaternions`
    coords: :class:`Coordinates`
    version: :class:`int`
    """
    identifier: str
    image_name: str
    image: SyncAsset | AsyncAsset | None = None  # type: ignore
    date: datetime
    caption: str
    centroid_coordinates: EarthLikeCoordinates
    dscovr_j2000_position: SpatialCoordinates
    lunar_j2000_position: SpatialCoordinates
    sun_j2000_position: SpatialCoordinates
    attitude_quaternions: AttitudeQuaternions
    coords: Coordinates
    version: int

    @property
    # i don't want to handle the logic wether to return a SyncAsset or an AsyncAsset
    # here since it would be bothersome
    def base_image(self) -> SyncAsset | AsyncAsset | None:
        """Optional[Union[:class:`SyncAsset`, :class:`AsyncAsset`]]: Returns the image as Asset."""
        return self.image
    
    @property
    def url(self) -> str:
        """:class:`str`: Builds and returns the url for the linked image."""
        return ""