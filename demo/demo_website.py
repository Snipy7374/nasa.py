from nasa import NasaSyncClient
from datetime import datetime

from flask import Flask
from flask import render_template

client = NasaSyncClient(token="DEMO_KEY")
app = Flask(__name__)

@app.route("/")
def apod():
    apod = client.get_astronomy_picture()
    return render_template("test.html", apod=apod, date=datetime.strftime(apod.date, "%Y-%m-%d"))

