from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import path

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False #utf-8

dbs = SQLAlchemy(app)

class Session(dbs.Model):
    __tablename__="session"
    id = dbs.Column(dbs.Integer, primary_key=True)
    user_id = dbs.Column(dbs.Integer, nullable=False)

