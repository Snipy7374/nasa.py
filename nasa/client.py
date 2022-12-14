from __future__ import annotations
from typing import overload, Generator

import logging
from datetime import datetime

from ._http import HTTPClient, Route
from .enums import Endpoints
from ._types import AstronomyPicture, RawAstronomyPicture
from .asset import SyncAsset


__all__: tuple[str, ...] = (
    "NasaSyncClient",
)

class NasaSyncClient:
    def __init__(self, *, token: str | None,
        #should_log: bool = False,
        #logging_level = LogLevels.INFO
    ) -> None:
        
        self.__token = token
        self._http = HTTPClient(self.__token)

    @overload
    def astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs: None) -> RawAstronomyPicture:
        ...
    
    @overload
    def astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs) -> list[RawAstronomyPicture]:
        ...

    def astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs) -> RawAstronomyPicture | list[RawAstronomyPicture]:
        return self._http.request(route=Route(method, endpoint), params=kwargs)

    def get_todays_astronomy_picture(self) -> AstronomyPicture:
        response = self.astronomy_request_impl("GET", Endpoints.APOD)
        return AstronomyPicture(**response, image=SyncAsset(response.get("url"), self._http))
    
    @staticmethod
    def _validate_date(date: str) -> bool:
        try:
            _date_validation = datetime.strptime(date, "%Y-%m-%d")
            return bool(_date_validation)
        except ValueError:
            raise ValueError("'date' parameter must follow the 'YYYY-mm-dd' date format")
    
    def get_astronomy_picture(self, date: datetime | str) -> AstronomyPicture:
        if not isinstance(date, (datetime, str)):
            raise ValueError(f"'date' must be of type 'str' or 'datetime.datetime' not {date.__class__!r}")
        if isinstance(date, datetime):
            date = datetime.strftime(date, "YYYY-mm-dd")
        
        self._validate_date(date)

        response = self.astronomy_request_impl("GET", Endpoints.APOD, date=date)
        return AstronomyPicture(**response, image=SyncAsset(response.get("url"), self._http)) # type: ignore i have an overload issue here, big skill issue

    def _get_multi_astronomy_pictures_impl(self, start_date: datetime | str, end_date: datetime | str | None = None) -> list[RawAstronomyPicture]:
        if not isinstance(start_date, (datetime, str)):
            raise ValueError(f"'start_date' must be of type 'str' or 'datetime.datetime' not {start_date.__class__!r}")
        if isinstance(start_date, datetime):
            start_date = datetime.strftime(start_date, "YYYY-mm-dd")
        self._validate_date(start_date)
        
        if end_date:
            if not isinstance(end_date, (datetime, str)):
                raise ValueError(f"'end_date' must be of type 'str' or 'datetime.datetime' not {end_date.__class__!r}")
            if isinstance(end_date, datetime):
                end_date = datetime.strftime(end_date, "YYYY-mm-dd")
            self._validate_date(end_date)
        
        return self.astronomy_request_impl("GET", Endpoints.APOD, start_date=start_date, end_date=end_date)


    def get_range_astronomy_pictures(self, start_date: datetime | str, end_date: datetime | str | None = None) -> list[AstronomyPicture]:
        response = self._get_multi_astronomy_pictures_impl(start_date, end_date)
        return [
            AstronomyPicture(**img_metadata, image=SyncAsset(img_metadata.get("url"), self._http))
            for img_metadata in response
        ]

    def get_gen_astronomy_pictures(self, start_date: datetime | str, end_date: datetime | str | None = None) -> Generator[AstronomyPicture,  None, None]:
        response = self._get_multi_astronomy_pictures_impl(start_date, end_date)
        for img_metadata in response:
            yield AstronomyPicture(**img_metadata, image=SyncAsset(img_metadata.get("url"), self._http))

        
