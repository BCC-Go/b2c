from session import Session, dbs
from datetime import datetime, timedelta
from app import *
from random import randint, shuffle

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

    def login(login_id, password):
        user = User.query.filter_by(login_id=login_id).first()
        if user.password == password:
            expires_in = timedelta(seconds=30)  # cookie 기간
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

    
    def have_point(user_id):
        point = Point.query.filter_by(user_id=user_id).all()
        return sum(point.point)

    def find_small_category(category_mid_id):
        cate_list = CategorySmall.query.filter_by(category_mid_id = category_mid_id).all()
        return [cate_list[randint(1,len(cate_list))].id, cate_list[randint(1,len(cate_list))].id]

    def recommand(recom,num):
        reco = UserFunction.find_small_category(recom.category_mid_id)
        items1 = shuffle(Product.query.filter_by(category_small_id = reco[0]).all())
        items2 = shuffle(Product.query.filter_by(category_small_id = reco[1]).all())
        result = []

        if num == 0 : # 모든 item 리턴
            range1 = len(items1)
            range2 = len(items2)
        else:
            range1 = num/2
            range2 = num-range1

        for i in range(1,range1):
            res = {}
            res['id'] = items1[i].id
            res['category_small_id'] = items1[i].category_small_id
            res['name'] = items1[i].name
            res['price'] = items1[i].price
            res['image'] = items1[i].image
            res['brand'] = items1[i].brand
            res['avg_star'] = items1[i].avg_star
            result.append(res)
        
        for i in range(1,range2):
            res = {}
            res['id'] = items2[i].id
            res['category_small_id'] = items2[i].category_small_id
            res['name'] = items2[i].name
            res['price'] = items2[i].price
            res['image'] = items2[i].image
            res['brand'] = items2[i].brand
            res['avg_star'] = items2[i].avg_star
            result.append(res)
        
        return result
    

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

