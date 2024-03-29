# nasa.py
<p align="center">
    <a href="https://github.com/Snipy7374/nasa.py/blob/master/LICENSE"><img alt="GitHub license file" src="https://img.shields.io/github/license/snipy7374/nasa.py?style=for-the-badge"></a>
    <a href="https://github.com/Snipy7374/nasa.py/commits/master"><img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/snipy7374/nasa.py?style=for-the-badge"></a>
</p>
Work in progress

to run the docs use 
```
sphinx-autobuild -a docs/source docs/_build/html --watch nasa
```

# Demo
![image](https://user-images.githubusercontent.com/100313469/207457548-06b74b8d-a95b-46a0-87fd-4a7103a5a2c6.png)

# Installation
Currently the package is not available on pypi, this means that you can't install it using just ``pip``.
To install ``Nasa.py`` you need to install ``git`` and to run this command
```
pip install git+https://github.com/Snipy7374/nasa.py
```

# Requirements
```
aiohttp
aiofiles
requests
```

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

This library also supports Async requests
```py
import typing as t
from nasa import NasaAsyncClient

if t.TYPE_CHECKING:
    from nasa import AstronomyPicture

client = NasaAsyncClient(token="TOKEN_HERE")

async def main():
    async with client:
        astronomy_picture: AstronomyPicture = await client.get_astronomy_picture()
        await astronomy_picture.image.save("image.png")
```

---
# Currently supported NASA API endpoints
- APOD (Astronomy picture of the day) - `/planetary/apod` - (all query parameters)

# TODO
- ~~Add `is_video` property on AstronomyPicture (based on `media_type`)~~
- ~~Add support for the `count` query parameter on `/planetary/apod` endpoint to get multiple random image~~
- ~~Solve typing issues with `typing.overload`s on `client.py`~~
- Support other endpoints
- ~~Add async client & methods~~
- Add logging
- ~~Add docs :)~~
- Add developing tools
- Add workflows on github
- Create the first release
- Upload the project on PyPi
- Customize the docs
- Add examples