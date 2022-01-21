from flask_session import Session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import session_path

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = session_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False #utf-8

db = SQLAlchemy(app)

class Session(db.Model):
    __tablename__="session"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    expire = db.Column(db.String(35), nullable=False)
    auth = db.Column(db.BINARY(1), nullable=False, server_default='0')

