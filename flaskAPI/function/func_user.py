from config.config_flask import timedelta
from model import *
from random import randint, shuffle

def access_cookie(session_id):
    session = Session.query.filter_by(id=session_id).first()
    if session.expire():
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
            expires = koreaNow() + expires_in
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

    def find_small_category(category_mid_id):
        cate_list = CategorySmall.query.filter_by(category_mid_id = category_mid_id).all()
        return [cate_list[randint(1,len(cate_list)-1)].id, cate_list[randint(1,len(cate_list)-1)].id]

    def recommand(id,num,type):
        if type == 'r':
            recom = UserRecommand.query.filter_by(user_id=id).first()
        else:
            recom = UserRecommand.query.filter_by(user_id=id).first()
        reco = UserFunction.find_small_category(recom.category_mid_id)
        items1 = Product.query.filter_by(category_small_id = reco[0]).all()
        items2 = Product.query.filter_by(category_small_id = reco[1]).all()
        item = items1+items2
        shuffle(item)
        if num == 0 or num > len(item):
            num = len(item)
    
        return all_item(item,num)

    def my_page(user):
        point = UserFunction.have_point(user.id)
        coupon = CouponUser.query.filter_by(user_id = user.id).all()
        coupon = len(coupon)
        result = {}
        result['name'] = user.name
        result['rank'] = user.rank.grade
        result['point'] = point
        result['coupon_num'] = coupon
        return result

    def have_point(user_id):
        point = []
        point = Point.query.filter_by(user_id=user_id).all()
        if len(point) == 0:
            return 0
        return sum(point.point)

    def coupon_list(user):
        coupon_user = CouponUser.query.filter_by(user_id=user.id).all()
        coupon_list=[]
        for item in coupon_user:
            coupon = CouponContent.query.filter_by(id=item.coupon_id).first()
            coupon_list.append(item_to_dict(coupon))
        return coupon_list


    # 좋아요 관련
    def list_like(user_id):
        like = Like.query.filter_by(user_id = user_id).all()
        result = []
        for item in like:
            product = Product.query.filter_by(id = item.product_id)
            result.append(item_to_dict(product))
        return result

    def add_like(user_id,product_id):
        like = Like(user_id = user_id, product_id = product_id)
        db.session.add(like)
        db.session.commit()

    def delete_like(uid,pid):
        like = Like.query.filter_by(user_id = uid , product_id = pid).first()
        #print(like.user_id)
        db.session.delete(like)
        db.session.commit()


    # 장바구니 관련
    def list_cart(user_id):
        cart = Cart.query.filter_by(user_id = user_id).all()
        return all_item(cart, len(cart))

    def add_cart(user_id,product_id):
        cart = Cart(user_id = user_id, product_id = product_id)
        db.session.add(cart)
        db.session.commit()

    def delete_cart(user_id,product_id):
        cart = Cart.query.filter_by(user_id = user_id).filter_by(product_id = product_id)
        db.session.delete(cart)
        db.session.commit()
