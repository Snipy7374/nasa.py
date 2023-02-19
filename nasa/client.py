from __future__ import annotations
from typing import (
    overload,
    Generator,
    AsyncGenerator,
    Any,
    TYPE_CHECKING,
    cast,
)

import logging
from datetime import datetime

from ._http import AsyncHTTPClient, HTTPClient, Route
from .enums import (
    Endpoints,
    EpicImageType,
    LogLevels,
    FileTypes
)
from ._types import (
    AstronomyPicture,
    EpicImage,
    EarthLikeCoordinates,
    SpatialCoordinates,
    AttitudeQuaternions,
    Coordinates,
)
from .asset import SyncAsset, AsyncAsset


if TYPE_CHECKING:
    from ._types import (
        RawAstronomyPicture,
        RawEpicImage,
    )

__all__: tuple[str, ...] = (
    "NasaSyncClient",
    "NasaAsyncClient",
)

_log = logging.getLogger(__name__)


class _BaseClient:
    """The base client class.
    
    .. note::
        This class is not available under the ``nasa`` namespace
        since it isn't meant to be used by users.

    """
    @staticmethod
    def _validate_date(date: str) -> datetime:
        """Create a datetime object from a string
        used internally for date validation and str to date
        conversions

        Parameters
        ----------
        date: :class:`str`
            The date to convert to a :class:`datetime.datetime` object.

        Raises
        ------
        ValueError
            If the ``date`` isn't in the ``YYYY-mm-dd`` date format.

        Returns
        -------
        :class:`datetime.datetime`
            The converted ``date``.
        """
        try:
            _date_validation = datetime.strptime(date, "%Y-%m-%d")
            return _date_validation
        except ValueError:
            raise ValueError("'date' parameter must follow the 'YYYY-mm-dd' date format")

    @staticmethod
    def _date_to_str(date: datetime) -> str:
        """Convert a datetime object into a string.
        
        Parameters
        ----------
        date: :class:`datetime.datetime`
            The ``date`` to convert.
        
        Returns
        -------
        :class:`str`
            The converted ``date``.
        """
        # i need this method since the API expects dates
        # with the format YYYY-mm-dd
        return datetime.strftime(date, "%Y-%m-%d")
    
    def _date_validator(self, start_date: datetime | str, end_date: datetime | str | None) -> tuple[str, str | None]:
        """
        Parameters
        ---------
        start_date: Union[:class:`datetime.datetime`, :class:`str`]
        end_date: Optional[Union[:class:`datetime.datetime`, :class:`str`]]

        Raises
            ValueError
                - If the parameters doesn't follows the respectives types.
                - If the format of the date doesn't follows the ``YYYY-mm-dd`` date format.
        """
        if not isinstance(start_date, (datetime, str)):
            raise ValueError(f"'start_date' must be of type 'str' or 'datetime.datetime' not {start_date.__class__!r}")

        if isinstance(start_date, datetime):
            start_date = datetime.strftime(start_date, "%Y-%m-%d")
        
        if not isinstance(end_date, (datetime, str)) and end_date is not None:
            raise ValueError(f"'end_date' must be of type 'datetime.datetime', 'str' or 'None' not {end_date.__class__!r}")

        if end_date:
            if not isinstance(end_date, (datetime, str)):
                raise ValueError(f"'end_date' must be of type 'str' or 'datetime.datetime' not {end_date.__class__!r}")
            if isinstance(end_date, datetime):
                end_date = datetime.strftime(end_date, "%Y-%m-%d")
        return (start_date, end_date)
    
    @staticmethod
    def _epic_url_image_builder(identifier: str, date: str, image_type: EpicImageType, image_as: str | None) -> tuple[str, str]:
        date = '/'.join(((date.split()[0]).split('-')))
        # split the date as %Y/%m/%d without converting it as datetime object

        image_type_ = "natural" if "natural" in image_type else "enhanced"
        prefix = "epic_1b" if image_type_ == "natural" else "epic_RGB"
        url = (
                f"{Endpoints.EPIC_IMG}/archive/{image_type_}/{date}/"+ (image_as if image_as else "{}") +
                f"/{prefix}_{identifier}." + (image_as if image_as else "{}")
            )
        return (url, "partial")



class NasaSyncClient(_BaseClient):
    """A synchronous client to make request to the NASA Api.

    This class can be used in context managers. See :ref:`NasaSyncClient-example-reference`
    for more informations.

    .. note::
        The session linked to this client does not necessarily
        need to be closed.

    .. warning::
        If you're planning to use this library in an asynchronous context
        you should use :class:`NasaAsyncClient`.

    .. versionadded:: 0.0.1

    Parameters
    ----------
    token: Optional[:class:`str`]
        The token that should be used to connect to the NASA Api.
    """
    def __init__(
        self,
        *,
        token: str | None,
        should_log: bool = False,
        logging_level: LogLevels = LogLevels.NOTSET
    ) -> None:
        self.__token = token
        self.__http = HTTPClient(token=self.__token)
        if not isinstance(logging_level, LogLevels):
            raise ValueError(f"'logging_level' must be an enum member of 'nasa.LogLevels' not {type(logging_level)}")
        self.logging_level = logging_level
        if should_log:
            logging.basicConfig(level=logging_level)
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.close()

    def close(self) -> None:
        """Closes the :class:`HTTPClient` session.
        
        .. caution::
            An :class:`HTTPClient` session cannot be re-opened.
        """
        _log.info("Closing the http client session")
        self.__http.close()
    
    @property
    def http_client(self) -> HTTPClient:
        """:class:`HTTPClient`: The ``HTTPClient`` linked to the :class:`NasaSyncClient` object."""
        return self.__http

    @overload
    def _astronomy_request_impl(self, method: str, endpoint: Endpoints, *, date: datetime | str | None) -> RawAstronomyPicture:
        ...
    
    @overload
    def _astronomy_request_impl(self, method: str, endpoint: Endpoints, *, start_date: datetime | str, end_date: datetime | str | None) -> list[RawAstronomyPicture]:
        ...
    
    @overload
    def _astronomy_request_impl(self, method: str, endpoint: Endpoints, *, count: int) -> list[RawAstronomyPicture]:
        ...

    def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs) -> RawAstronomyPicture | list[RawAstronomyPicture]:
        return self.__http.request(route=Route(method, endpoint), params=kwargs)
    
    def get_astronomy_picture(self, date: datetime | str | None = None) -> AstronomyPicture:
        """Fetch an :class:`AstronomyPicture` of a given date.
        If ``date`` is not provided returns the todays' astronomy picture.

        Parameters
        ---------
        date: Optional[Union[:class:`datetime.datetime`, :class:`str`]]
            If not provided defaults to todays' date.
        
        Raises
        ------
        ValueError
            The ``date`` doesn't follows the ``YYYY-mm-dd`` date format.

        Returns
        ------
        :class:`AstronomyPicture`
            An astronomy picture.
        """
        if date and not isinstance(date, (datetime, str)):
            raise ValueError(f"'date' must be of type 'str' or 'datetime.datetime' not {date.__class__!r}")
        if isinstance(date, datetime):
            date = datetime.strftime(date, "%Y-%m-%d")

        if date:
            self._validate_date(date)

        response = self._astronomy_request_impl("GET", Endpoints.APOD, date=date)
        return AstronomyPicture(
            copyright=response.get("copyright", None),
            date=cast(datetime, response["date"]),
            explanation=response["explanation"],
            hdurl=response.get("hdurl", None),
            media_type=response.get("media_type", None),
            service_version=response["service_version"],
            title=response["title"],
            url=response["url"],
            image=SyncAsset(
                response.get("url"),
                self.__http,
                "full"
            )
        )

    def _get_multi_astronomy_pictures_impl(self, start_date: datetime | str, end_date: datetime | str | None = None) -> list[RawAstronomyPicture]:
        start_date, end_date = self._date_validator(start_date, end_date)
        return self._astronomy_request_impl("GET", Endpoints.APOD, start_date=start_date, end_date=end_date)


    def get_range_astronomy_pictures(self, start_date: datetime | str, end_date: datetime | str | None = None) -> list[AstronomyPicture]:
        """Fetch multiple images with a given date range and
        return a :class:`list` of :class:`AstronomyPicture`.

        Parameters
        ---------
        start_date: Union[:class:`datetime.datetime`, :class:`str`]
            The start date. If provided as string it must follow the ``YYYY-mm-dd``
            date format.
        end_date: Optional[Union[:class:`datetime.datetime`, :class:`str`]]
            The end date. If provided as string it must follow the ``YYYY-mm-dd``
            date format. If not provided defaults to todays' date.
        
        Returns
        ------
        List[:class:`AstronomyPicture`]
            A list of astronomy pictures for the required date range.
        """
        response = self._get_multi_astronomy_pictures_impl(start_date, end_date)
        return [
            AstronomyPicture(
                copyright=img_metadata.get("copyright", None),
                date=cast(datetime, img_metadata["date"]),
                explanation=img_metadata["explanation"],
                hdurl=img_metadata.get("hdurl", None),
                media_type=img_metadata.get("media_type", None),
                service_version=img_metadata["service_version"],
                title=img_metadata["title"],
                url=img_metadata["url"],
                image=SyncAsset(
                    img_metadata.get("url"),
                    self.__http,
                    "full",
                )
            )
            for img_metadata in response
        ]

    def get_gen_astronomy_pictures(self, start_date: datetime | str, end_date: datetime | str | None = None) -> Generator[AstronomyPicture,  None, None]:
        """Fetch multiple images with a given date range and
        return a ``generator`` of :class:`AstronomyPicture`.
        
        Parameters
        ---------
        start_date: Union[:class:`datetime.datetime`, :class:`str`]
            The start date. If provided as string it must follow the ``YYYY-mm-dd``
            date format.
        end_date: Optional[Union[:class:`datetime.datetime`, :class:`str`]]
            The end date. If provided as string it must follow the ``YYYY-mm-dd``
            date format. If not provided defaults to todays' date.
        
        Yields
        ------
        :class:`AstronomyPicture`
        """
        response = self._get_multi_astronomy_pictures_impl(start_date, end_date)
        for img_metadata in response:
            yield AstronomyPicture(
                copyright=img_metadata.get("copyright", None),
                date=cast(datetime, img_metadata["date"]),
                explanation=img_metadata["explanation"],
                hdurl=img_metadata.get("hdurl", None),
                media_type=img_metadata.get("media_type", None),
                service_version=img_metadata["service_version"],
                title=img_metadata["title"],
                url=img_metadata["url"],
                image=SyncAsset(
                    img_metadata.get("url"),
                    self.__http,
                    "full",
                )
            )
    
    def get_rand_astronomy_pictures(self, count: int = 1) -> list[AstronomyPicture]:
        """Fetch a random number of astronomy pictures.

        Parameters
        ---------
        count: :class:`int`
            The number of random astronomy pictures to fetch.
            Must be between 1 and 100 (both inclusive).

        Returns
        ------
        List[:class:`AstronomyPicture`]
            A list of random astronomy pictures.
        """
        if not isinstance(count, int):
            raise ValueError(f"'count' must be of type 'int' not {count.__class__!r}")
        
        if not 1 <= count <= 100:
            raise ValueError(f"'count' must be a number beetween 1 and 100")
        response = self._astronomy_request_impl("GET", Endpoints.APOD, count=count)

        return [
            AstronomyPicture(
                copyright=img_metadata.get("copyright", None),
                date=cast(datetime, img_metadata["date"]),
                explanation=img_metadata["explanation"],
                hdurl=img_metadata.get("hdurl", None),
                media_type=img_metadata.get("media_type", None),
                service_version=img_metadata["service_version"],
                title=img_metadata["title"],
                url=img_metadata["url"],
                image=SyncAsset(
                    img_metadata.get("url"),
                    self.__http,
                    "full",
                )
            )
            for img_metadata in response
        ]


    """ Asteroids things that i'm not sure to implement

    def get_asteroids_with_date_range(self, start_date: datetime | str, end_date: datetime | str | None = None):
        self._date_validator(start_date, end_date)
        if isinstance(start_date, datetime):
            start_date = self._date_to_str(start_date)
        if isinstance(end_date, datetime):
            end_date = self._date_to_str(end_date)
        payload: dict[str, str] = {
            "start_date": start_date,
        }
        if end_date:
            payload["end_date"] = end_date
        return self._http.request(route=Route("GET", Endpoints.NEOWS + "feed"), params=payload)
    
    def get_asteroid(self, asteroid_id: int):
        if not isinstance(asteroid_id, int):
            raise ValueError
        
        url = Endpoints.NEOWS + f"neo/{asteroid_id}"
        
        return self._http.request(route=Route("GET", Endpoints.NEOWS + "neo/"), params={})
    """

    def _epic_impl(self, method: str, endpoint: str, **kwargs) -> list[RawEpicImage]:
        if not kwargs.get("date"):
            del kwargs["date"]
        
        # i need to url encode things
        if kwargs.get("date"):
            endpoint += f"/{kwargs.get('date')}"
        return self.__http.request(route=Route(method, endpoint))
    
    def get_epic_images(
        self,
        date: datetime | None = None,
        *,
        image_type: EpicImageType = EpicImageType.natural,
        image_as: FileTypes | None = None
    ) -> list[EpicImage]:
        """Fetch earth images from the EPIC endpoint.

        .. versionadded:: 0.0.1 

        Parameters
        ----------
        date: Optional[:class:`datetime.datetime`]
            If not provided fetchs the default :class:`EpicImage`\s returned
            by the Nasa API.
        image_type: :class:`EpicImageType`
            Defaults to :attr:`EpicImageType.natural`.
        image_as: Optional[:class:`FileTypes`]
            The file extension of the image. This can be a png, a jpg or a thumbs.
        
        Returns
        -------
        list[:class:`EpicImage`] Returns the requested epic images.
        """
        date_ = self._date_to_str(datetime.now())
        if date:
            date_ = self._date_to_str(date)

        response = self._epic_impl(method="GET", endpoint=Endpoints.EPIC + image_type, date=date_)
        return [
            EpicImage(
                identifier=epic.get("identifier"),
                image_name=epic["image"],
                image=SyncAsset(
                    url=(_u := self._epic_url_image_builder(
                            identifier=epic.get("identifier"),
                            date=epic["date"],
                            image_type=image_type,
                            image_as=image_as,
                        )
                    )[0],
                    http_client=self.__http,
                    url_state=_u[1]
                ),
                date=epic["date"],
                caption=epic["caption"],
                centroid_coordinates=EarthLikeCoordinates(**epic["centroid_coordinates"]),
                dscovr_j2000_position=SpatialCoordinates(**epic["dscovr_j2000_position"]),
                lunar_j2000_position=SpatialCoordinates(**epic["lunar_j2000_position"]),
                sun_j2000_position=SpatialCoordinates(**epic["sun_j2000_position"]),
                attitude_quaternions=AttitudeQuaternions(**epic["attitude_quaternions"]),
                coords=Coordinates(
                    centroid_coordinates=EarthLikeCoordinates(**epic["coords"]["centroid_coordinates"]),
                    dscovr_j2000_position=SpatialCoordinates(**epic["coords"]["dscovr_j2000_position"]),
                    lunar_j2000_position=SpatialCoordinates(**epic["coords"]["lunar_j2000_position"]),
                    sun_j2000_position=SpatialCoordinates(**epic["coords"]["sun_j2000_position"]),
                    attitude_quaternions=AttitudeQuaternions(**epic["coords"]["attitude_quaternions"])
                ),
                version=epic["version"],
                image_type=image_type
            ) 
            for epic in response
        ]


class NasaAsyncClient(_BaseClient):
    """An asynchronous client to make request to the NASA Api.

    .. note::

        This class can also be used as context manager.

        .. code-block:: python3

            from nasa import NasaAsyncClient

            async def main():
                async with NasaAsyncClient(token="token") as client:
                    image = await client.get_astronomy_picture()
        
        This will handle automatically the :class:`HTTPClient` closure.
        For more information see :ref:`NasaAsyncClient-example-reference`

    .. warning::
        You need to manually close the session linked to the this
        client using :func:`close`.

    .. versionadded:: 0.0.1

    Parameters
    ----------
    token: Optional[:class:`str`]
        The token that should be used to connect to the NASA Api.
    """
    def __init__(
        self,
        *,
        token: str | None,
        should_log: bool = False,
        logging_level: LogLevels = LogLevels.NOTSET
    ) -> None:
        self.__token = token
        self.__http = AsyncHTTPClient(token=self.__token)
        if not isinstance(logging_level, LogLevels):
            raise ValueError(f"'logging_level' must be an enum member of 'nasa.LogLevels' not {type(logging_level)}")
        self.logging_level = logging_level
        if should_log:
            logging.basicConfig(level=logging_level)
    
    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback):
        await self.__http.close()
    
    async def close(self):
        """Closes the :class:`HTTPClient` session.
        
        .. caution::
            An :class:`HTTPClient` session cannot be re-opened.
        """
        _log.info("Closing the http client session")
        await self.__http.close()
    
    @property
    def http_client(self) -> AsyncHTTPClient:
        """:class:`HTTPClient`: The ``HTTPClient`` linked to the :class:`NasaAsyncClient` object."""
        return self.__http
    
    @overload
    async def _astronomy_request_impl(self, method: str, endpoint: Endpoints) -> RawAstronomyPicture:
        ...

    @overload
    async def _astronomy_request_impl(self, method: str, endpoint: Endpoints, *, date: datetime | str | None) -> RawAstronomyPicture:
        ...
    
    @overload
    async def _astronomy_request_impl(self, method: str, endpoint: Endpoints, *, start_date: datetime | str, end_date: datetime | str | None) -> list[RawAstronomyPicture]:
        ...
    
    @overload
    async def _astronomy_request_impl(self, method: str, endpoint: Endpoints, *, count: int) -> list[RawAstronomyPicture]:
        ...

    async def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs) -> RawAstronomyPicture | list[RawAstronomyPicture]:
        return await self.__http.request(route=Route(method, endpoint), params=kwargs)

    async def get_astronomy_picture(self, date: datetime | str | None = None) -> AstronomyPicture:
        """Fetch an :class:`AstronomyPicture` of a given date.
        If ``date`` is not provided returns the todays' astronomy picture.

        Parameters
        ----------
        date: Optional[Union[:class:`datetime.datetime`, :class:`str`]]
            If not provided defaults to todays' date.

        Raises
        ------
        ValueError
            The ``date`` doesn't follows the ``YYYY-mm-dd`` date format.

        Returns
        -------
        :class:`AstronomyPicture`
            An astronomy picture.
        """
        if date and not isinstance(date, (datetime, str)):
            raise ValueError(f"'date' must be of type 'str' or 'datetime.datetime' not {date.__class__!r}")
        if isinstance(date, datetime):
            date = datetime.strftime(date, "%Y-%m-%d")

        if date:
            self._validate_date(date)
            response = await self._astronomy_request_impl("GET", Endpoints.APOD, date=date)
        else:
            response = await self._astronomy_request_impl("GET", Endpoints.APOD)
        return AstronomyPicture(**response, image=AsyncAsset(response.get("url"), self.__http)) # type: ignore i have an overload issue here, big skill issue

    async def _get_multi_astronomy_pictures_impl(self, start_date: datetime | str, end_date: datetime | str | None = None) -> list[RawAstronomyPicture]:
        start_date, end_date = self._date_validator(start_date, end_date)
        return await self._astronomy_request_impl("GET", Endpoints.APOD, start_date=start_date, end_date=end_date or "")  # aiohttp won't accept a 'None' parameter idk why

    async def get_range_astronomy_pictures(self, start_date: datetime | str, end_date: datetime | str | None = None) -> list[AstronomyPicture]:
        """Fetch multiple images with a given date range and
        return a :class:`list` of :class:`AstronomyPicture`.

        Parameters
        ----------
        start_date: Union[:class:`datetime.datetime`, :class:`str`]
            The start date. If provided as string it must follow the ``YYYY-mm-dd``
            date format.
        end_date: Optional[Union[:class:`datetime.datetime`, :class:`str`]]
            The end date. If provided as string it must follow the ``YYYY-mm-dd``
            date format. If not provided defaults to todays' date.
        
        Returns
        -------
        List[:class:`AstronomyPicture`]
            A list of astronomy pictures for the required date range.
        """
        response = await self._get_multi_astronomy_pictures_impl(start_date, end_date)
        return [
            AstronomyPicture(
                copyright=img_metadata.get("copyright", None),
                date=cast(datetime, img_metadata["date"]),
                explanation=img_metadata["explanation"],
                hdurl=img_metadata.get("hdurl", None),
                media_type=img_metadata.get("media_type", None),
                service_version=img_metadata["service_version"],
                title=img_metadata["title"],
                url=img_metadata["url"],
                image=AsyncAsset(
                    img_metadata.get("url"),
                    self.__http,
                    "full"
                )
            )
            for img_metadata in response
        ]

    async def get_gen_astronomy_pictures(self, start_date: datetime | str, end_date: datetime | str | None = None) -> AsyncGenerator[AstronomyPicture, None]:
        """Fetch multiple images with a given date range and
        return an asynchronous ``generator`` of :class:`AstronomyPicture`.
        
        Parameters
        ---------
        start_date: Union[:class:`datetime.datetime`, :class:`str`]
            The start date. If provided as string it must follow the ``YYYY-mm-dd``
            date format.
        end_date: Optional[Union[:class:`datetime.datetime`, :class:`str`]]
            The end date. If provided as string it must follow the ``YYYY-mm-dd``
            date format. If not provided defaults to todays' date.
        
        Yields
        ------
        :class:`AstronomyPicture`
        """
        response = await self._get_multi_astronomy_pictures_impl(start_date, end_date)
        for img_metadata in response:
            yield AstronomyPicture(
                copyright=img_metadata.get("copyright", None),
                date=cast(datetime, img_metadata["date"]),
                explanation=img_metadata["explanation"],
                hdurl=img_metadata.get("hdurl", None),
                media_type=img_metadata.get("media_type", None),
                service_version=img_metadata["service_version"],
                title=img_metadata["title"],
                url=img_metadata["url"],
                image=AsyncAsset(
                    img_metadata.get("url"),
                    self.__http,
                    "full",
                )
            )
    
    async def get_rand_astronomy_pictures(self, count: int = 1) -> list[AstronomyPicture]:
        """Fetch a random number of astronomy pictures.

        Parameters
        ---------
        count: :class:`int`
            The number of random astronomy pictures to fetch.
            Must be between 1 and 100 (both inclusive).

        Returns
        ------
        List[:class:`AstronomyPicture`]
            A list of random astronomy pictures.
        """
        if not isinstance(count, int):
            raise ValueError(f"'count' must be of type 'int' not {count.__class__!r}")
        
        if not 1 <= count <= 100:
            raise ValueError(f"'count' must be a number beetween 1 and 100")
        response = await self._astronomy_request_impl("GET", Endpoints.APOD, count=count)

        return [
            AstronomyPicture(
                copyright=img_metadata.get("copyright", None),
                date=cast(datetime, img_metadata["date"]),
                explanation=img_metadata["explanation"],
                hdurl=img_metadata.get("hdurl", None),
                media_type=img_metadata.get("media_type", None),
                service_version=img_metadata["service_version"],
                title=img_metadata["title"],
                url=img_metadata["url"],
                image=AsyncAsset(
                    img_metadata.get("url"),
                    self.__http,
                    "full",
                )
            )
            for img_metadata in response
        ]
    
    async def _epic_impl(self, method: str, endpoint: str, **kwargs) -> list[RawEpicImage]:
        if not kwargs.get("date"):
            del kwargs["date"]
        
        # i need to url encode things
        if kwargs.get("date"):
            endpoint += f"/{kwargs.get('date')}"
        return await self.__http.request(route=Route(method, endpoint))
    
    async def get_epic_images(
        self,
        date: datetime | None = None,
        *,
        image_type: EpicImageType = EpicImageType.natural,
        image_as: FileTypes | None = None
    ) -> list[EpicImage]:
        """Fetch earth images from the EPIC endpoint.

        .. versionadded:: 0.0.1 

        Parameters
        ----------
        date: Optional[:class:`datetime.datetime`]
            If not provided fetchs the default :class:`EpicImage`\s returned
            by the Nasa API.
        image_type: :class:`EpicImageType`
            Defaults to :attr:`EpicImageType.natural`.
        image_as: Optional[:class:`FileTypes`]
            The file extension of the image. This can be a png, a jpg or a thumbs.
        
        Returns
        -------
        list[:class:`EpicImage`] Returns the requested epic images.
        """
        date_ = self._date_to_str(datetime.now())
        if date:
            date_ = self._date_to_str(date)

        response = await self._epic_impl(method="GET", endpoint=Endpoints.EPIC + image_type, date=date_)
        return [
            EpicImage(
                identifier=epic.get("identifier"),
                image_name=epic["image"],
                image=AsyncAsset(
                    url=(_u := self._epic_url_image_builder(
                            identifier=epic.get("identifier"),
                            date=epic["date"],
                            image_type=image_type,
                            image_as=image_as,
                        )
                    )[0],
                    http_client=self.__http,
                    url_state=_u[1]
                ),
                date=epic["date"],
                caption=epic["caption"],
                centroid_coordinates=EarthLikeCoordinates(**epic["centroid_coordinates"]),
                dscovr_j2000_position=SpatialCoordinates(**epic["dscovr_j2000_position"]),
                lunar_j2000_position=SpatialCoordinates(**epic["lunar_j2000_position"]),
                sun_j2000_position=SpatialCoordinates(**epic["sun_j2000_position"]),
                attitude_quaternions=AttitudeQuaternions(**epic["attitude_quaternions"]),
                coords=Coordinates(
                    centroid_coordinates=EarthLikeCoordinates(**epic["coords"]["centroid_coordinates"]),
                    dscovr_j2000_position=SpatialCoordinates(**epic["coords"]["dscovr_j2000_position"]),
                    lunar_j2000_position=SpatialCoordinates(**epic["coords"]["lunar_j2000_position"]),
                    sun_j2000_position=SpatialCoordinates(**epic["coords"]["sun_j2000_position"]),
                    attitude_quaternions=AttitudeQuaternions(**epic["coords"]["attitude_quaternions"])
                ),
                version=epic["version"],
                image_type=image_type
            ) 
            for epic in response
        ]