from config.config_flask import timedelta
from function.func_view import ProductFunc
from model import *

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

def product_preview(item, n, uid):
    res = item_to_dict(item[0])
    res.update(item_to_dict(item[1]))
    ProductFunc.discount(res,item[0].id, uid)
    return res

class UserFunction():
    def login(login_id, password):
        user = User.query.filter_by(login_id=login_id).first()
        if user:
            if user.password == password:
                expires_in = timedelta(hours=3)  # cookie 기간
                expires = koreaNow() + expires_in
                session = Session(user_id = user.id, expires = expires)
                db.session.add(session)
                db.session.commit()
                return session.id
        return 0

    def logout(uid):
        user = Session.query.filter_by(user_id=uid).first()
        db.session.delete(user)
        db.session.commit()

    def regist(login_id, password, name, phone, sex, birth, address):
        if User.query.filter_by(login_id=login_id).first():
            return 'id is already'
        user = User(rank_id = b'\x31', login_id = login_id, password = password, name = name, phone = phone, sex = int(sex), birth = birth, consumption = 0, address = address, type = b'\x00')
        db.session.add(user)
        db.session.commit()
        return 1

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

    def have_point(user_id): # point 총액
        point = []
        point = Point.query.filter_by(user_id=user_id).all()
        if len(point) == 0:
            return 0
        return sum(point.point)

    def point_list(user_id): # point 리스트
        point = Point.query.filter_by(user_id=user_id).all()
        return all_item(point, len(point))

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
            product = db.session.query(Product,ProductDetail).filter(Product.id == ProductDetail.product_id, Product.id == item.product_id).first()
            result.append(product_preview(product,1,user_id))
        return result

    def add_like(user_id,product_id):
        like = Like(user_id = user_id, product_id = product_id)
        db.session.add(like)
        db.session.commit()

    def delete_like(uid,pid):
        like = Like.query.filter_by(user_id = uid , product_id = pid).first()
        db.session.delete(like)
        db.session.commit()


    # 장바구니 관련
    def list_cart(user_id):
        cart = Cart.query.filter_by(user_id = user_id).all()
        result = []
        for item in cart:
            product = db.session.query(Product,ProductDetail).filter(Product.id == ProductDetail.product_id, Product.id == item.product_id).first()
            result.append(product_preview(product,1,user_id))
        return result

    def add_cart(user_id,product_id):
        cart = Cart(user_id = user_id, product_id = product_id)
        db.session.add(cart)
        db.session.commit()

    def delete_cart(uid,pid):
        cart = Cart.query.filter_by(user_id = uid , product_id = pid).first()
        db.session.delete(cart)
        db.session.commit()


    #리뷰 관련
    def regist_review_img(uid,pid,content,image,star): # 등록
        item = Product.query.filter_by(id = pid).first()
        
        last = db.session.query(Review.id).order_by(Review.id.desc()).first()
        if last is None:
            num = 0
        else:
            num = last[0]
        if upload_image(image,num,'review/'):
            img = 'review/'+str(num+1)+splitext(file.filename)[1]
        review = Review(user_id = uid, product_id = pid, content = content, image = img, star = star, write_time = koreaNow())
        re = db.session.query(Review.star).filter(Review.product_id == pid).all()
        re = [re[i][0] for i in range(len(re))]
        re.append(star)
        avg_star = sum(re)/len(re)
        item.avg_star = avg_star
        db.session.add(review)
        db.session.commit()
    
    def regist_review(uid,pid,content,star): # 등록

        review = Review(user_id = uid, product_id = pid, content = content, image = '', star = star, write_time = koreaNow())
        db.session.add(review)
        re = db.session.query(Review.star).filter(Review.product_id == pid).all()
        re = [re[i][0] for i in range(len(re))]
        re.append(star)
        avg_star = sum(re)/len(re)

        item = Product.query.filter_by(id = pid).first()
        item.avg_star = avg_star
        db.session.commit()

    def load_review(pid): # 보여주기
        review = Review.query.filter_by(product_id = pid).all()
        result = []
        for item in review:
            name = db.session.query(User.name).filter(User.id == item.user_id).first()
            uname = name[0][0]+'*'+name[0][2:]
            item = item_to_dict(item)
            item['name'] = uname
            result.append(item)
        return result


    #질문 관련
    def regist_question(uid,pid,title,content,hashtag): # 등록
        question = Question(user_id = uid, product_id = pid, titel = title, content = content, hashtag = hashtag, write_time = koreaNow())
        db.session.add(question)
        db.session.commit()

    def load_question(pid): # 보여주기
        question = db.session.query(Question,Answer).filter(Question.product_id == pid, Question.id == Answer.question_id).all()
        result = []
        dict = lambda r: {r.__table__.name+'_'+c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
        for item in question:
            res = dict(item[0])
            name = db.session.query(User.name).filter(User.id == item[1].user_id).first()
            uname = name[0][0]+'*'+name[0][2:]
            res['name'] = uname
            res.update(dict(item[1]))
            result.append(res)

    def answer_question(writer,qid, content): # 답변 등록
        if writer.type == 0:
            return 0
        answer = Answer(question_id = qid, user_id = writer.id, content = content, write_time = koreaNow())
        db.session.add(answer)
        db.session.commit()
        return 1
