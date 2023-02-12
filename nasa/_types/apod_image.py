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
    """Represents a received payload from the APOD endpoint.

    .. versionadded:: 0.0.1

    Attributes
    ----------
    copyright: Optional[:class:`str`]
        The copyright of the linked file.
    date: :class:`str`
        The date back when the file was the astronomy picture
        of the day.
    explanation: :class:`str`
        A short description about the file.
    hdurl: Optional[:class:`str`]
        The high quality url to the file.
    media_type: :class:`str`
        The type of media of the file. This can be either
        ``"image"`` or ``"video"``.
    service_version: :class:`str`
        The version of the api.
    title: :class:`str`
        The title of the file.
    url: :class:`str`
        The url to the file.
    """
    copyright: str | None
    date: str
    explanation: str
    hdurl: str | None
    media_type: str
    service_version: str
    title: str
    url: str


def convert_to_date(string: str) -> datetime:
    return datetime.strptime(string, "%Y-%m-%d")


@attrs.define(kw_only=True, repr=True, eq=True)
class AstronomyPicture:
    """Represents an apod image object returned by the NASA Api.

    .. versionadded:: 0.0.1

    Attributes
    ----------
    copyright: Optional[:class:`str`]
        The copyright of the linked file.
    date: :class:`datetime.datetime`
        The date back when the file was the astronomy picture
        of the day.
    explanation: :class:`str`
        A short description about the file.
    hdurl: Optional[:class:`str`]
        The high quality url to the file.
    media_type: Optional[:class:`str`]
        The type of media of the file. This can be either
        ``"image"`` or ``"video"``.

        .. admonition:: Todo
            :class: admonition-todo

            Transform this attribute in an enum member or flag.
    service_version: :class:`str`
        The version of the api.
    title: :class:`str`
        The title of the file.
    url: :class:`str`
        The url to the file.
    image: Union[:class:`SyncAsset`, :class:`AsyncAsset`]
        The file represented as a python object. This is useful if
        you're trying to fetch the bytes of the file or to save the file.

        .. note::
            The type of asset depends on what type of client you're using.
            With a :class:`NasaSyncClient` you'll get a :class:`SyncAsset` viceversa
            with a :class:`NasaAsyncClient` you'll get an :class:`AsyncAsset`.

        .. tab:: Save a file

            .. admonition:: Example

                .. code-block:: python3

                    client = NasaAsyncClient(token="...")
                    image: AstronomyPicture = await client.get_astronomy_picture()
                    # this will save the image with the "title" as
                    # its name
                    await image.save(image.title)
        
        .. tab:: Fetch bytes of an asset

            .. admonition:: Example

                .. code-block:: python3

                    apod_obj: AstronomyPicture = await client.get_astronomy_picture()
                    # if "bytes_asset" is None then our bytes aren't cached so we fetch the file
                    # this example assumes that you're using the NasaAsyncClient
                    image_bytes = apod_obj.bytes_asset or await apod_obj.image.read()
                
                .. caution::
                    :attr:`AsyncAsset.bytes_asset` can be ``None`` if the bytes of the asset aren't cached yet.
                    You must handle that case yourself as shown above.
    """
    copyright: str | None = None
    date: datetime = attrs.field(converter=convert_to_date)
    explanation: str
    hdurl: str | None = None
    media_type: str | None = None
    service_version: str
    title: str
    url: str
    image: SyncAsset | AsyncAsset 
    # i feel like this could be typed in a better way

    @property
    def is_video(self) -> bool:
        """:class:`bool`: Whether the ``url`` lead to a video or not."""
        return not self.media_type == "image"
    
    @property
    def is_image(self) -> bool:
        """:class:`bool`: Whether the ``url`` lead to an image or not."""
        return self.media_type == "image"
