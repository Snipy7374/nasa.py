from enum import Enum

__all__: tuple[str, ...] = (
    "Endpoints",
    "EpicImageType",
    "LogLevels",
    "FileTypes",
)

class Endpoints(str, Enum):
    APOD = "/planetary/apod"
    NEOWS = "/neo/rest/v1/"
    EPIC = "/EPIC/api/"
    EPIC_IMG = "https://epic.gsfc.nasa.gov"


class EpicImageType(str, Enum):
    natural = "natural"
    natural_date = "natural/date"
    natural_all = "natural/all"
    natural_available = "natural/available"
    enhanced = "enhanced"
    enhanced_date = "enhanced/date"
    enhanced_all = "enhanced/all"
    enhanced_available = "enhanced/available"


class FileTypes(str, Enum):
    png = "png"
    jpg = "jpg"
    thumbs = "thumbs"


class LogLevels(int, Enum):
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0