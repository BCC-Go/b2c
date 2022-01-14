from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import path

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__="user"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)


