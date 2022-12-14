# nasa.py
WIP

# Demo

# Basic usage
Create a client object
```py
import typing as t
from nasa import Client

if t.TYPE_CHECKING:
    from nasa import AstronomyPicture

client = Client(token="TOKEN_HERE")
```
get the todays astronomy picture
```py
astronomy_picture: AstronomyPicture = client.get_astronomy_picture()
```
save an image
```py
astronomy_picture.image.save("image.png")
```
---
# Currently supported NASA API endpoints
- APOD (Astronomy picture of the day) - `/planetary/apod` - (all query parameters)

# TODO
- Add `is_video` property on AstronomyPicture (based on `media_type`)
- Add support for the `count` query parameter on `/planetary/apod` endpoint to get multiple random image
- Solve typing issues with `typing.overload`s on `client.py`
- Support other endpoints
- Add docs :) 