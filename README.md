# nasa.py
WIP

# Demo
![image](https://user-images.githubusercontent.com/100313469/207457548-06b74b8d-a95b-46a0-87fd-4a7103a5a2c6.png)

# Basic usage
```py
from nasa import Client

c = Client(token="TOKEN_HERE")
img = c.get_astronomy_picture("2022-12-13")

asset = img.image.save("image.png", seek_at_end=False)
```
