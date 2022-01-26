from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import path

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False #utf-8

db = SQLAlchemy(app)

# 유저 관련 테이블
class User(db.Model): # 유저
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    rank_id = db.Column(db.BINARY(1), db.ForeignKey('rank.id'), nullable=False)
    loginId = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(15), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    sex = db.Column(db.BINARY(1), nullable=False)
    birth = db.Column(db.String(8), nullable=False)
    consumption = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    type = db.Column(db.BINARY(1), nullable=False)

    point = db.relationship('Point', backref='user', lazy=True)
    coupon_user = db.relationship('CouponUser', backref='user', lazy=True)
    recommand = db.relationship('UserRecommand', backref='user', lazy=True)
    taste = db.relationship('UserTaste', backref='user', lazy=True)
    like = db.relationship('Like', backref='user', lazy=True)
    cart = db.relationship('Cart', backref='user', lazy=True)
    review = db.relationship('Review', backref='user', lazy=True)
    question = db.relationship('Question', backref='user', lazy=True)
    buylist = db.relationship('Buylist', backref='user', lazy=True)
    
class UserRecommand(db.Model): # 유저 비슷한 상품
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    category_mid_id = db.Column(db.Integer, db.ForeignKey('category_mid.id'), nullable=False)

class UserTaste(db.Model): # 유저 취향 상품
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    category_mid_id = db.Column(db.Integer, db.ForeignKey('category_mid.id'), nullable=False)

class Rank(db.Model): # 등급
    __tablename__="rank"
    id = db.Column(db.BINARY(1), primary_key=True)
    consumption = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(45), nullable=False)

    rank = db.relationship('User', backref='rank', lazy=True)

class Point(db.Model): # 포인트
    __tablename__="point"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    point = db.Column(db.BINARY(6), nullable=False)
    content = db.Column(db.String(100))

class CouponContent(db.Model): # 쿠폰 내용
    __tablename__="coupon_content"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    expire = db.Column(db.String(35), nullable=False) 

    coupon_content = db.relationship('CouponUser', backref='coupon_content', lazy=True)
    
class CouponUser(db.Model): # 유저가 가진 쿠폰
    __tablename__="coupon_user"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupon_content.id'), primary_key=True)
    


# 상품 관련 테이블
class Product(db.Model): # 상품
    __tablename__="product"
    id = db.Column(db.Integer, primary_key=True)
    category_small_id = db.Column(db.Integer, db.ForeignKey('category_small.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(45), nullable=False)
    brand = db.Column(db.String(45), nullable=False)
    avg_star = db.Column(db.Float, nullable=False)
    regist_time = db.Column(db.String(35), nullable=False) 

    detail = db.relationship('ProductDetail', backref='product', lazy=True)
    discount = db.relationship('Discount', backref='product', lazy=True)
    like = db.relationship('Like', backref='product', lazy=True)
    cart = db.relationship('Cart', backref='product', lazy=True)
    review = db.relationship('Review', backref='product', lazy=True)
    question = db.relationship('Question', backref='product', lazy=True)
    buylist = db.relationship('Buylist', backref='product', lazy=True)

class ProductDetail(db.Model): # 상품 상세 설명
    __tablename__="product_detail"
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    summary = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.String(200), nullable=False)
    
class Discount(db.Model): # 상품 할인 정보
    __tablename__="discount"
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    start_date = db.Column(db.String(35), nullable=False)
    end_date = db.Column(db.String(35), nullable=False)
    rate = db.Column(db.Float, nullable=False)

class Event(db.Model):
    __tablename__="event"
    event_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    image = db.Column(db.String(45), nullable=False)
    expire = db.Column(db.String(35), nullable=False)

# 유저 상품 관련 테이블
class Like(db.Model): # 좋아요
    __tablename__="like"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

class Cart(db.Model): # 장바구니
    __tablename__="cart"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

class Review(db.Model): # 리뷰
    __tablename__="review"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    content = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(45), nullable=False)
    star = db.Column(db.Float, nullable=False)
    write_time = db.Column(db.String(35), nullable=False)

class Question(db.Model): # 질문
    __tablename__="question"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    hashtag = db.Column(db.String(30), nullable=False)
    write_time = db.Column(db.String(35), nullable=False)

    answer = db.relationship('Answer', backref='question', lazy=True)

class Answer(db.Model): # 질문
    __tablename__="answer"
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # user type : 2(판매자)
    content = db.Column(db.String(500), nullable=False)
    write_time = db.Column(db.String(35), nullable=False)

class Buylist(db.Model): # 구매목록
    __tablename__="buylist"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    count = db.Column(db.BINARY(5), nullable=False)
    write_time = db.Column(db.String(35), nullable=False)



# 카테고리 관련 테이블
class CategorySmall(db.Model):
    __tablename__="category_small"
    id = db.Column(db.Integer, primary_key=True)
    category_mid_id = db.Column(db.Integer, db.ForeignKey('category_mid.id'), nullable=False)
    name = db.Column(db.String(45), nullable=False)

    category = db.relationship('Product', backref='category_small', lazy=True)

class CategoryMid(db.Model):
    __tablename__="category_mid"
    id = db.Column(db.Integer, primary_key=True)
    category_large_id = db.Column(db.Integer, db.ForeignKey('category_large.id'), nullable=False)
    name = db.Column(db.String(45), nullable=False)

    category = db.relationship('CategorySmall', backref='category_mid', lazy=True)
    recommand = db.relationship('UserRecommand', backref='category_mid', lazy=True)
    taste = db.relationship('UserTaste', backref='category_mid', lazy=True)

class CategoryLarge(db.Model):
    __tablename__="category_large"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    image = db.Column(db.String(45), nullable=False)

    category = db.relationship('CategoryMid', backref='category_large', lazy=True)
