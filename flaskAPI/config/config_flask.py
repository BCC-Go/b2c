from flask import Flask
from config.config_db import path
from datetime import timedelta, datetime

app = Flask(__name__, static_url_path='/static')

app.config["SQLALCHEMY_DATABASE_URI"] = path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False #utf-8
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAX_CONTENT_PATH'] = 40


def koreaNow():
    ko = timedelta(hours=9)
    return datetime.now() + ko