from session import Session, dbs
from datetime import datetime, timedelta
from app import *

def access_cookie(session_id):
    # session_id = request.cookies.get('session_id')
    # expires = request.cookies.get('Expires')
    session = Session.query.filter_by(id=session_id).first()
    if session.id & session.expire():
        return session.user_id # success
    dbs.session.delete(session)
    dbs.session.commit()
    return 0 # fail 재발급 해야함

class UserFunction():
    def session_check(session_id):
        user_id = access_cookie(session_id)
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return user.id

    def login(login_id, password):
        user = User.query.filter_by(login_id=login_id).first()
        if user.password == password:
            expires_in = timedelta(hours=1)  # cookie 기간
            expires = datetime.now() + expires_in
            session = Session(user_id = user.id, expires = expires)
            dbs.session.add(session)
            dbs.session.commit()
            return session.id
        return 0

    def regist(login_id, password, name, phone, sex, birth, address):
        if User.query.filter_by(login_id==login_id):
            return 'id is already'
        user = User(rank_id = 1, login_id = login_id, password = password, name = name, phone = phone, sex = int(sex), birth = birth, consumption = 0, address = address, type = 0)
        db.session.add(user)
        db.session.commit()
        return 1