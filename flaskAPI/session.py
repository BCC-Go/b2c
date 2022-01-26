from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import path
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False #utf-8

dbs = SQLAlchemy(app)

class Session(dbs.Model):
    __tablename__="session"
    id = dbs.Column(dbs.Integer, primary_key=True)
    user_id = dbs.Column(dbs.Integer, nullable=False)
    expire = dbs.Column(dbs.String(35), nullable=False)

    # session 만료
    def expire(self):
        now = datetime.now()
        diff = str(self.expire - now)
        if diff[4] == '-': # 현재시간이 만료를 지났으면 diff = expires로 설정되어 2022- ~~로 나옴
            return 0
        return 1
