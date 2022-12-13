from __future__ import annotations
from typing import Literal, TypedDict, Union

class LogNOTSET(TypedDict):
    level: Literal[0]

class LogDEBUG(TypedDict):
    level: Literal[10]

class LogINFO(TypedDict):
    level: Literal[20]


