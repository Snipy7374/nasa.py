from __future__ import annotations
from typing import TYPE_CHECKING

import logging
from datetime import datetime

from ._http import HTTPClient, Route
from .enums import Endpoints
from ._types import AstronomyPicture, RawAstronomyPicture


__all__: tuple[str, ...] = (
    "Client",
)

class Client:
    def __init__(self, *, token: str | None,
        #should_log: bool = False,
        #logging_level = LogLevels.INFO
    ) -> None:
        
        self.__token = token
        self._http = HTTPClient(self.__token)

    def astronomy_request_impl(self, method: str, endpoint: Endpoints, **kwargs) -> RawAstronomyPicture:
        return self._http.request(route=Route(method, endpoint), params=kwargs)
    
    def get_todays_astronomy_picture(self) -> AstronomyPicture:
        return AstronomyPicture(**self.astronomy_request_impl("GET", Endpoints.APOD))
    
    def get_astronomy_picture(self, date: datetime | str) -> AstronomyPicture:
        if not isinstance(date, (datetime, str)):
            raise ValueError(f"'date' must be of type 'str' or 'datetime.datetime' not {date.__class__!r}")
        if isinstance(date, datetime):
            date = datetime.strftime(date, "YYYY-mm-ddd")
        
        try:
            _date_validation = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("'date' parameter must follow the 'YYYY-mm-dd' date format")
        
        return AstronomyPicture(**(self.astronomy_request_impl("GET", Endpoints.APOD, date=date)))
