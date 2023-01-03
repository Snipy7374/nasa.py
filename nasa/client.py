from __future__ import annotations
from typing import overload, Generator, AsyncGenerator

import logging
from datetime import datetime

from ._http import AsyncHTTPClient ,HTTPClient, Route
from .enums import Endpoints
from ._types import AstronomyPicture, RawAstronomyPicture
from .asset import SyncAsset, AsyncAsset


__all__: tuple[str, ...] = (
    "NasaSyncClient",
    "NasaAsyncClient",
)


class _BaseClient:
    @staticmethod
    def _validate_date(date: str) -> datetime:
        """Create a datetime object from a string
        used internally for date validation and str to date
        conversions
        """
        try:
            _date_validation = datetime.strptime(date, "%Y-%m-%d")
            return _date_validation
        except ValueError:
            raise ValueError("'date' parameter must follow the 'YYYY-mm-dd' date format")

    @staticmethod
    def _date_to_str(date: datetime) -> str:
        """Convert a datetime object into a strgin"""
        # i need this method since the API expects dates
        # with the format YYYY-mm-dd
        return datetime.strftime(date, "%Y-%m-%d")
    
    def _date_validator(self, start_date: datetime | str, end_date: datetime | str | None) -> None:
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
    def __init__(self, *, token: str | None,
        #should_log: bool = False,
        #logging_level = LogLevels.INFO
    ) -> None:
        
        self.__token = token
        self.__http = HTTPClient(token=self.__token)

    @overload
    def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs: None) -> RawAstronomyPicture:
        ...
    
    @overload
    def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs) -> list[RawAstronomyPicture]:
        ...

    def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs) -> RawAstronomyPicture | list[RawAstronomyPicture]:
        return self.__http.request(route=Route(method, endpoint), params=kwargs)
    
    def get_astronomy_picture(self, date: datetime | str | None = None) -> AstronomyPicture:
        """Get an AstronomyPicture
        
        Parameters

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
        response = self._get_multi_astronomy_pictures_impl(start_date, end_date)
        for img_metadata in response:
            yield AstronomyPicture(**img_metadata, image=SyncAsset(img_metadata.get("url"), self.__http))
    
    def get_rand_astronomy_pictures(self, count: int = 1) -> list[AstronomyPicture]:
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


class NasaAsyncClient(_BaseClient):
    def __init__(self, *, token: str | None) -> None:
        self.__token = token
        self.__http = AsyncHTTPClient(token=self.__token)
    
    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback):
        await self.__http.close()
    
    @overload
    async def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs: None) -> RawAstronomyPicture:
        ...
    
    @overload
    async def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs) -> list[RawAstronomyPicture]:
        ...

    async def _astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs) -> RawAstronomyPicture | list[RawAstronomyPicture]:
        return await self.__http.request(route=Route(method, endpoint), params=kwargs)

    async def get_astronomy_picture(self, date: datetime | str | None = None) -> AstronomyPicture:
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
        response = await self._get_multi_astronomy_pictures_impl(start_date, end_date)
        for img_metadata in response:
            yield AstronomyPicture(**img_metadata, image=AsyncAsset(img_metadata.get("url"), self.__http))
    
    async def get_rand_astronomy_pictures(self, count: int = 1) -> list[AstronomyPicture]:
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

    async def close(self):
        await self.__http.close()