from nasa import NasaSyncClient
from datetime import datetime

from flask import Flask
from flask import render_template

from redis_cache import redis, cache

client = NasaSyncClient(token="DEMO_KEY")
app = Flask(__name__)

REDIS_EXPIRE_TIME_IN_SECONDS = 3600

@app.route("/")
@cache("apod")
def apod(cache, key):
    if cache is None:
        apod = client.get_astronomy_picture()
        redis.set(name=key, value=apod, ex=REDIS_EXPIRE_TIME_IN_SECONDS)
    else:
        apod = cache
    return render_template("test.html", apod=apod, date=datetime.strftime(apod.date, "%Y-%m-%d"))

