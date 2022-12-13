from nasa import Client


c = Client(token="TOKEN_HERE")
img = c.get_astronomy_picture("2022-12-13")

asset = img.image.save("image.png", seek_at_end=False)