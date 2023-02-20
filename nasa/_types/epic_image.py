from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

import attrs
from datetime import datetime

from ..asset import AsyncAsset, SyncAsset

if TYPE_CHECKING:
    from ..enums import EpicImageType

__all__: tuple[str, ...] = (
    "RawEpicImage",
    "RawSpatialCoordinates",
    "RawEarthLikeCoordinates",
    "RawAttitudeQ",
    "EpicCoordinates",
    "SpatialCoordinates",
    "EarthLikeCoordinates",
    "AttitudeQuaternions",
    "Coordinates",
    "EpicImage",
    "AvailableDates",
)


def convert_to_date(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


class RawSpatialCoordinates(TypedDict):
    """Represents a :class:`SpatialCoordinates` raw payload.

    .. versionadded:: 0.0.1

    Attributes
    ----------
    x: :class:`float`
    y: :class:`float`
    z: :class:`float`
    """
    x: str
    y: str
    z: str


class RawEarthLikeCoordinates(TypedDict):
    """Represents a :class:`EarthLikeCoordinates` raw payload.

    .. versionadded:: 0.0.1

    Attributes
    ----------
    lat: :class:`float`
        Represents the latitude.
    lon: :class:`float`
        Represents the longitude.
    """
    lat: str
    lon: str


class RawAttitudeQ(TypedDict):
    """Rpresents a :class:`AttitudeQuaternions` raw payload.

    .. versionadded:: 0.0.1

    Attributes
    ----------
    q0: :class:`float`
    q1: :class:`float`
    q2: :class:`float`
    q3: :class:`float`
    """
    q0: str
    q1: str
    q2: str
    q3: str


class EpicCoordinates(TypedDict):
    """Represents a :class:`Coordinates` raw payload.

    .. versionadded:: 0.0.1

    Attributes
    ----------
    centroid_coordinates: :class:`RawEarthLikeCoordinates`
        Geographical coordinates that the satellite is looking at.
    dscovr_j2000_position: :class:`RawSpatialCoordinates`
        Position of the satellite in space.
    lunar_j2000_position: :class:`RawSpatialCoordinates`
        Position of the moon in space.
    sun_j2000_position: :class:`RawSpatialCoordinates`
        Position of the sun in space.
    attitude_quaternions: :class:`RawAttitudeQ`
        Satellite attitude.
    """
    centroid_coordinates: RawEarthLikeCoordinates
    dscovr_j2000_position: RawSpatialCoordinates
    lunar_j2000_position: RawSpatialCoordinates
    sun_j2000_position: RawSpatialCoordinates
    attitude_quaternions: RawAttitudeQ


class AvailableDates(TypedDict):
    available_dates: list[str]


class RawEpicImage(TypedDict):
    """Represents an EPIC object returned by the NASA Api.

    .. versionadded:: 0.0.1

    Attributes
    ----------
    identifier: :class:`str`
        The identifier linked to the returned EPIC object.
    image: :class:`str`
        The image name of the photo shooted by the satellite.
    date: :class:`str`
        The date of the image.
    caption: :class:`str`
        The caption of the image.
    centroid_coordinates: :class:`RawEarthLikeCoordinates`
        Geographical coordinates that the satellite is looking at.
    dscovr_j2000_position: :class:`RawSpatialCoordinates`
        Position of the satellite in space.
    lunar_j2000_position: :class:`RawSpatialCoordinates`
        Position of the moon in space.
    sun_j2000_position: :class:`RawSpatialCoordinates`
        Position of the sun in space.
    attitude_quaternions: :class:`RawAttitudeQ`
        Satellite attitude.
    coords: :class:`EpicCoordinates`
        Coordinates linked to the postion of the satellite.
    version: :class:`int`
        The Api version.
    """
    identifier: str
    image: str
    date: str
    caption: str
    centroid_coordinates: RawEarthLikeCoordinates
    dscovr_j2000_position: RawSpatialCoordinates
    lunar_j2000_position: RawSpatialCoordinates
    sun_j2000_position: RawSpatialCoordinates
    attitude_quaternions: RawAttitudeQ
    coords: EpicCoordinates
    version: str


@attrs.define(kw_only=True, repr=True)
class SpatialCoordinates:
    """Represents spatial coordinates using xyz axes.

    .. versionadded:: 0.0.1

    Attributes
    ----------
    x: :class:`float`
        Represents the x axis.
    y: :class:`float`
        Represents the y axis.
    z: :class:`float`
        Represents the z axis.
    """
    x: str = attrs.field(converter=float)
    y: str = attrs.field(converter=float)
    z: str = attrs.field(converter=float)


@attrs.define(kw_only=True, repr=True)
class EarthLikeCoordinates:
    """Represents coordinates based on the earth
    coordinates system.
    
    .. versionadded:: 0.0.1

    Attributes
    ----------
    lat: :class:`float`
        Represents the latitude.
    lon: :class:`float`
        Represents the longitude.
    """
    lat: str = attrs.field(converter=float)
    lon: str = attrs.field(converter=float)


@attrs.define(kw_only=True, repr=True)
class AttitudeQuaternions:
    """Represents satellite attitude.

    .. versionadded:: 0.0.1

    Attributes
    ----------
    q0: :class:`float`
    q1: :class:`float`
    q2: :class:`float`
    q3: :class:`float`
    """
    q0: str = attrs.field(converter=float)
    q1: str = attrs.field(converter=float)
    q2: str = attrs.field(converter=float)
    q3: str = attrs.field(converter=float)


@attrs.define(kw_only=True, repr=True, eq=True)
class Coordinates:
    """Groups coordinates of differents objects.

    .. versionadded:: 0.0.1

    Attributes
    ----------
    centroid_coordinates: :class:`EarthLikeCoordinates`
        Geographical coordinates that the satellite is looking at.
    dscovr_j2000_position: :class:`SpatialCoordinates`
        Position of the satellite in space.
    lunar_j2000_position: :class:`SpatialCoordinates`
        Position of the moon in space.
    sun_j2000_position: :class:`SpatialCoordinates`
        Position of the sun in space.
    attitude_quaternions: :class:`AttitudeQuaternions`
        Satellite attitude.
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
        The identifier linked to the returned EPIC object.
        This is used to build the url.
    image_name: :class:`str`
        The name of the image.
    image: Optional[Union[:class:`SyncAsset`, :class:`AsyncAsset`]]
        The image as asset if available.
    date: :class:`datetime.datetime`
        The date of the image.
    caption: :class:`str`
        The caption of the image.
    centroid_coordinates: :class:`EarthLikeCoordinates`
        Geographical coordinates that the satellite is looking at.
    dscovr_j2000_position: :class:`SpatialCoordinates`
        Position of the satellite in space.
    lunar_j2000_position: :class:`SpatialCoordinates`
        Position of the moon in space.
    sun_j2000_position: :class:`SpatialCoordinates`
        Position of the sun in space.
    attitude_quaternions: :class:`AttitudeQuaternions`
        Satellite attitude.
    coords: :class:`Coordinates`
        Coordinates linked to the postion of the satellite.
    version: :class:`int`
        The Api version.
    """
    identifier: str
    image_name: str
    image: SyncAsset | AsyncAsset | None = None  # type: ignore
    date: str = attrs.field(converter=convert_to_date)
    caption: str
    centroid_coordinates: EarthLikeCoordinates
    dscovr_j2000_position: SpatialCoordinates
    lunar_j2000_position: SpatialCoordinates
    sun_j2000_position: SpatialCoordinates
    attitude_quaternions: AttitudeQuaternions
    coords: Coordinates
    version: str = attrs.field(converter=int)
    image_type: EpicImageType

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