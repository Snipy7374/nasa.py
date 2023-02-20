from typing import NamedTuple, Literal

import logging

from .client import *
from .enums import *
from .asset import *
from ._types import *

__name__ = "nasa.py"
__author__ = "Snipy7374"
__copyright__ = "2022-present Snipy7374"
__license__ = "MIT"
__version__ = "0.0.2a"


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release_level: Literal["alpha", "beta", "final"]

version_info: VersionInfo = VersionInfo(major=0, minor=0, micro=2, release_level="alpha")

logger = logging.getLogger(__name__)