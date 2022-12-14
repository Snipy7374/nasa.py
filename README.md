# nasa.py
WIP

# Demo
![image](https://user-images.githubusercontent.com/100313469/207457548-06b74b8d-a95b-46a0-87fd-4a7103a5a2c6.png)

# Basic usage
Create a client object
```py
import typing as t
from nasa import NasaSyncClient

if t.TYPE_CHECKING:
    from nasa import AstronomyPicture

client = NasaSyncClient(token="TOKEN_HERE")
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
- ~~Add `is_video` property on AstronomyPicture (based on `media_type`)~~
- ~~Add support for the `count` query parameter on `/planetary/apod` endpoint to get multiple random image~~
- Solve typing issues with `typing.overload`s on `client.py`
- Support other endpoints
- Add async client & methods
- Add logging
- Add docs :)
- Add developing tools
- Add workflows on github
