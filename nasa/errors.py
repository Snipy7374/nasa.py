
class NasaException(Exception):
    pass


class HTTPException(NasaException):
    def __init__(self, response, message: str) -> None:
        self.response = response

        super().__init__()