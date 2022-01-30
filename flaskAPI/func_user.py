from session import Session, dbs
from datetime import datetime, timedelta
from app import *
from random import randint, shuffle

def access_cookie(session_id):
    # session_id = request.cookies.get('session_id')
    # expires = request.cookies.get('Expires')
    print(session_id)
    session = Session.query.filter_by(id=session_id).first()
    if session.id & session.expire():
        return session.user_id # success
    db.session.delete(session)
    db.session.commit()
    return 0 # fail 재발급 해야함

item_to_dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
def all_item(item, n):
    result = []
    for i in range(n):
        result.append(item_to_dict(item[i]))

    return result


class UserFunction():

    def login(login_id, password):
        user = User.query.filter_by(login_id=login_id).first()
        if user.password == password:
            expires_in = timedelta(minutes=2)  # cookie 기간
            expires = datetime.now() + expires_in
            session = Session(user_id = user.id, expires = expires)
            db.session.add(session)
            db.session.commit()
            return session.id
        return 0

    def regist(login_id, password, name, phone, sex, birth, address):
        if User.query.filter_by(login_id==login_id):
            return 'id is already'
        user = User(rank_id = 1, login_id = login_id, password = password, name = name, phone = phone, sex = int(sex), birth = birth, consumption = 0, address = address, type = 0)
        db.session.add(user)
        db.session.commit()
        return 1

    
    def have_point(user_id):
        point = Point.query.filter_by(user_id=user_id).all()
        return sum(point.point)

    def find_small_category(category_mid_id):
        cate_list = CategorySmall.query.filter_by(category_mid_id = category_mid_id).all()
        return [cate_list[randint(1,len(cate_list)-1)].id, cate_list[randint(1,len(cate_list)-1)].id]

    def recommand(recom,num):
        reco = UserFunction.find_small_category(recom.category_mid_id)
        items1 = Product.query.filter_by(category_small_id = reco[0]).all()
        items2 = Product.query.filter_by(category_small_id = reco[1]).all()
        item = items1+items2
        shuffle(item)
        if num == 0 or num > len(item):
            num = len(item)
    
        return all_item(item,num)
    

class CategoryView():
    def show_category_all():
        category = CategoryLarge.query.all()
        result = []
        for i in range(1,len(category)):
            res = {}
            res['id'] = category[i].id
            res['name'] = category[i].id
            res['result'] = category[i].id
            result.append(res)
        return result
    
    # def show_item():

