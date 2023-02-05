from __future__ import annotations
from typing import (
    overload,
    Generator,
    AsyncGenerator,
    Any,
    TYPE_CHECKING,
)

import logging
from datetime import datetime

from ._http import AsyncHTTPClient, HTTPClient, Route
from .enums import Endpoints
from ._types import (
    AstronomyPicture,
    EpicImage,
    EarthLikeCoordinates,
    SpatialCoordinates,
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
    
    def _date_validator(self, start_date: datetime | str, end_date: datetime | str | None) -> None:
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
            start_date = datetime.strftime(start_date, "YYYY-mm-dd")
        self._validate_date(start_date)
        
        if not isinstance(end_date, (datetime, str)) and end_date is not None:
            raise ValueError(f"'end_date' must be of type 'datetime.datetime', 'str' or 'None' not {end_date.__class__!r}")

        if end_date:
            if not isinstance(end_date, (datetime, str)):
                raise ValueError(f"'end_date' must be of type 'str' or 'datetime.datetime' not {end_date.__class__!r}")
            if isinstance(end_date, datetime):
                end_date = datetime.strftime(end_date, "YYYY-mm-dd")
            self._validate_date(end_date)



class NasaSyncClient(_BaseClient):
    """A synchronous client to make request to the NASA Api.

    .. warning::
        If you're planning to use this library in an asynchronous context
        you should use :class:`NasaAsyncClient`.

    .. versionadded:: 0.0.1

    Parameters
    ---------
    token: Optional[:class:`str`]
        The token that should be used to connect to the NASA Api.
    """
    def __init__(self, *, token: str | None,
        #should_log: bool = False,
        #logging_level = LogLevels.INFO
    ) -> None:
        self.__token = token
        self.__http = HTTPClient(token=self.__token)
    
    @property
    def http_client(self) -> HTTPClient:
        """:class:`HTTPClient`: The ``HTTPClient`` linked to the :class:`NasaSyncClient` object."""
        return self.__http

    @overload
    def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs) -> RawAstronomyPicture:
        ...
    
    @overload
    def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs) -> list[RawAstronomyPicture]:
        ...

    def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs: dict[str, Any]) -> RawAstronomyPicture | list[RawAstronomyPicture]:
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
            date = datetime.strftime(date, "YYYY-mm-dd")

        if date:
            self._validate_date(date)

        response = self._astronomy_request_impl("GET", Endpoints.APOD, date=date)
        return AstronomyPicture(**response, image=SyncAsset(response.get("url"), self.__http)) # type: ignore i have an overload issue here, big skill issue

    def _get_multi_astronomy_pictures_impl(self, start_date: datetime | str, end_date: datetime | str | None = None) -> list[RawAstronomyPicture]:
        self._date_validator(start_date, end_date)
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
                **img_metadata,
                image=SyncAsset(img_metadata.get("url"), self.__http
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
            yield AstronomyPicture(**img_metadata, image=SyncAsset(img_metadata.get("url"), self.__http))
    
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
                **img_metadata,
                image=SyncAsset(img_metadata.get("url"), self.__http
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

    def _epic_impl(self, method: str, endpoint: Endpoints, **kwargs: dict[str, Any]) -> RawEpicImage | list[RawEpicImage]:
        return self.__http.request(route=Route(method, endpoint), params=kwargs)
    
    def get_epic_images(self, date: datetime | None = None) -> EpicImage | list[EpicImage]:
        pass
        #self._epic_impl(method="GET")

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
    
    .. seealso::
        To manually close the session use :func:`close`.

    .. versionadded:: 0.0.1

    Parameters
    ----------
    token: Optional[:class:`str`]
        The token that should be used to connect to the NASA Api.
    """
    def __init__(self, *, token: str | None) -> None:
        self.__token = token
        self.__http = AsyncHTTPClient(token=self.__token)
    
    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback):
        await self.__http.close()
    
    async def close(self):
        """Closes the :class:`HTTPClient` session.
        
        .. caution::
            An :class:`HTTPClient` session cannot be re-opened.
        """
        await self.__http.close()
    
    @property
    def http_client(self) -> AsyncHTTPClient:
        """:class:`HTTPClient`: The ``HTTPClient`` linked to the :class:`NasaAsyncClient` object."""
        return self.__http
    
    @overload
    async def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs: None) -> RawAstronomyPicture:
        ...
    
    @overload
    async def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs) -> list[RawAstronomyPicture]:
        ...

    async def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs: dict[str, Any]) -> RawAstronomyPicture | list[RawAstronomyPicture]:
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
            date = datetime.strftime(date, "YYYY-mm-dd")

        if date:
            self._validate_date(date)
            response = await self._astronomy_request_impl("GET", Endpoints.APOD, date=date)
        else:
            response = await self._astronomy_request_impl("GET", Endpoints.APOD)
        return AstronomyPicture(**response, image=AsyncAsset(response.get("url"), self.__http)) # type: ignore i have an overload issue here, big skill issue

    async def _get_multi_astronomy_pictures_impl(self, start_date: datetime | str, end_date: datetime | str | None = None) -> list[RawAstronomyPicture]:
        self._date_validator(start_date, end_date)
        return await self._astronomy_request_impl("GET", Endpoints.APOD, start_date=start_date, end_date=end_date)

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
                **img_metadata,
                image=AsyncAsset(img_metadata.get("url"), self.__http
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
            yield AstronomyPicture(**img_metadata, image=AsyncAsset(img_metadata.get("url"), self.__http))
    
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
                **img_metadata,
                image=AsyncAsset(img_metadata.get("url"), self.__http
                )
            )
            for img_metadata in response
        ]