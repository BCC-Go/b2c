from flask import make_response, jsonify, request
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger
from flask_cors import CORS
from model import app, db, User
from function.func_user import UserFunction, access_cookie
from function.func_view import CategoryView, ProductFunc
from function.func_img import Image

CORS(app,supports_credentials=True)
api = Api(app)
swagger = Swagger(app)

class Login(Resource):
    def post(self):
        """
        login with id, password. return is login_cookie
        please send cookie on header all request
        ---
        tags:
          - Login
        parameters:
          - in: body
            name: login_id
            type: string
            requirement: true
          - in: body
            name: password
            type: string
            requirement: true
        responses:
            200:
                description: cookie in request header
        """
        data = request.get_json()
        print(request.headers['Session'])
        session = UserFunction.login(data['login_id'],data['password'])
        if session == 0:
            return "Not Found"
        
        resp = make_response(jsonify({'session_id': session}))
        resp.set_cookie('session_id',str(session))
        return resp

class Logout(Resource):
    def put(self):
        """
        delete cookie 
        ---
        tags:
          - Logout

        responses:
            200:
                description: cookie is expired
        """
        session_id = request.cookies.get('session_id')
        db.session.delete(Session.query.filter_by(id=session_id).first())
        db.session.commit()
        response = make_response('logout')
        return response

class Regist(Resource):
    def post(self):
        """
        회원가입 요청
        password must be encryption(SHA-256) before send
        ---
        tags:
          - Regist
        parameters:
          - in: formData
            name: loginId
            type: string
            requirement: true
          - in: formData
            name: password
            type: string
            requirement: true
          - in: formData
            name: phone
            type: string
            description: 01012345678 no dash(-)
            requirement: true
          - in: formData
            name: sex
            type: binary
            description: 0 = man & 1 = female
            requirement: true
          - in: formData
            name: birth
            type: string
            description: only 8 number ex.20001020
            requirement: true
          - in: formData
            name: address
            type: string
            requirement: true
          - in: formData
            name: taste
            type: string
            requirement: true
            responses:
              200:
                description: 성공하면 로그인 페이지로 이동
        """
        data = request.get_json()
        value = UserFunction.regist(login_id = data['login_id'], password = data['password'], name = data['name'], phone = data['phone'], sex = int(data['sex']), birth = data['birth'], address = data['address'])
        if 1 == value:
            return "",200
        return value

class EventBanner(Resource):
    def get(self):
        """
        메인페이지 event banner
        ---
        tags:
          - EventBanner
        responses:
            200:
                description: 성공 시 event img url return
                schemas:
                    properties:
                        img_url:
                            type:string
        """
        return 200

class Mypage(Resource):
    def get(self):
        """
        마이페이지
        로그인 안할 시 이용 불가
        ---
        tags:
          - Mypage
        responses:
            200:
                schema:
                    id: mypage
                    properties:
                        name: 
                            type: string
                        rank:
                            type: string
                            description: 유저 등급
                        point:
                            type: int
                            description: 보유중인 포인트 총액 수
                        coupon_num:
                            type: int
                            description: 보유중인 쿠폰 수
        """
        session_id = request.headers['Session']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.my_page(user)

class CouponList(Resource):
    def get(self):
        """
        보유한 쿠폰 리스트 반환
        쿠폰 이름, 내용, 만료 날짜 반환
        ---
        tags:
          - Mypage
        responses:
            200:
                schema:
                    id: couponlist
                    properties:
                        name:
                            type: string
                        content:
                            type: string
                        expire:
                            type: string
        """
        session_id = request.headers['Session']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.coupon_list(user)

class PointList(Resource):
    def get(self):
        """
        보유한 쿠폰 리스트 반환
        쿠폰 이름, 내용, 만료 날짜 반환
        ---
        tags:
          - Mypage
        responses:
            200:
                schema:
                    id: pointlist
                    properties:
                        point:
                            type: int
                        content:
                            type: string
        """
        session_id = request.headers['Session']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.point_list(user)

class ImageUpload(Resource):
    def post(self):
        """
        이벤트 이미지 업로드
        ---
        tags:
          - ImageUpload
        parameters:
          - in: body
            name: url
            type: string
        responses:
            200:
                description: upload success

        """
        data = request.get_json()
        Image.upload(data['url'])

        return "success"

class Like(Resource):
    def get(self):
        """
        좋아요 상품 리스트
        ---
        tags:
          - Like
        responses:
            200:
                description: 유저가 좋아요한 상품 리스트 보여주기
                schema:
                    id: product view  
        """
        session_id = request.headers['Session']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.list_like(user.id)

    def post(self):
        """
        상품에 좋아요 하기
        ---
        tags:
          - Like
        parameters:
          - in: body
            name: product_id
            type: int
            requirement: true
        responses:
            200:
                description: 상품 좋아요 성공
        """
        session_id = request.headers['Session']
        data = request.get_json()
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.add_like(user.id,data['product_id'])

    def delete(self,pid):
        """
        상품에 좋아요 취소
        ---
        tags:
          - Like
        parameters:
          - in: path
            type: int
            requirement: true
        responses:
            200:
                description: 상품 좋아요 취소 성공
        """
        session_id = request.headers['Session']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.delete_like(user.id,pid)

class Cart(Resource):
    def get(self):
        """
        좋아요 상품 리스트
        ---
        tags:
          - Cart
        responses:
            200:
                description: 유저가 좋아요한 상품 리스트 보여주기
                schema:
                    id: product view  
        """
        session_id = request.headers['Session']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.list_cart(user.id)

    def post(self):
        """
        상품에 좋아요 하기
        ---
        tags:
          - Cart
        parameters:
          - in: body
            name: product_id
            type: int
            requirement: true
        responses:
            200:
                description: 상품 좋아요 성공
        """
        session_id = request.headers['Session']
        data = request.get_json()
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.add_cart(user.id,data['product_id'])

    def delete(self,pid):
        """
        상품에 좋아요 취소
        ---
        tags:
          - Cart
        parameters:
          - in: path
            type: int
            requirement: true
        responses:
            200:
                description: 상품 좋아요 취소 성공
        """
        session_id = request.headers['Session']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.delete_cart(user.id,pid)

class ItemRegist(Resource):
    def post(self):
        """
        상품에 좋아요 하기
        ---
        tags:
          - Producer
        parameters:
          - in: body
            name: category_name
            type: string
            requirement: true
            description: 카테고리 이름
          - in: body
            name: name
            type: string
            requirement: true
            description: 이름
          - in: body
            name: price
            type: int
            requirement: true
            description: 가격
          - in: body
            name: image
            type: string
            requirement: true
            description: 이미지 url 주소
          - in: body
            name: brand
            type: string
            requirement: true
            description: brand 이름
          - in: body
            name: summary
            type: string
            requirement: true
            description: 상품 요약 설명
          - in: body
            name: detail
            type: string
            requirement: true
            description: 상품 상세 설명
        responses:
            200:
                description: 상품 좋아요 성공
        """
        session_id = request.headers['Session']
        data = request.get_json()
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return ProductFunc.regist_product(user, data['category_name'], data['name'], data['price'], data['image'], data['brand'], data['summary'], data['detail'])

class ProductRecommand(Resource):
    def get(self):
        """
        메인페이지 추천상품
        로그인 안했으면 로그인을 하면 더 자세한 상품을 볼 수 있다고 표시
        ---
        tags:
          - MainPage
        responses:
            0:
                description: 비 로그인 시 0 리턴
            200:
                description: 로그인 인증
                schema:
                    id: product view 
                    properties:
                        id:
                            type: int
                            description: product_id
                        category_small_id:
                            type: int
                            description: 최하위 카테고리 id
                        name:
                            type: string
                            description: 상품 이름
                            price:
                            type: int
                            description: 상품 가격
                        image:
                            type: string
                            description: 상품 이미지 url
                        brand:
                            type: string
                            description: 상품 brand 이름
                        avg_star:
                            type: Folat
                            description: 상품 평균 별점
                        summary:
                            type: string
                            description: 상품 요약 설명
        """

        session_id = request.headers['Session']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return ProductFunc.recommand(user.id,12,'r')

class ProductTaste(Resource):
    def get(self):
        """
        메인페이지 취향상품
        로그인 안했으면 로그인을 하면 더 자세한 상품을 볼 수 있다고 표시
        ---
        tags:
          - MainPage
        responses:
            200:
                description: 로그인 인증
                schema:
                    id: product view
        """
        session_id = request.cookies.get('session_id')
        user_id = access_cookie(session_id)
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return ProductFunc.recommand(user.id,12,'t')

class Search(Resource):
    def get(self,kw):
        """
        item 검색
        검색어를 path에 싫어 보냄
        ---
        tags:
          - Search
        parameters:
          - in: path
            type: string
            description: 검색어 문자열
        responses:
            200:
                description: 로그인 인증
                schema:
                    id: product view
        """
        session_id = request.cookies.get('session_id')
        user_id = access_cookie(session_id)
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return Search.search_key(user.id,kw)

class SearchCurrent(Resource):
    def get(self,kw):
        """
        item 검색
        검색어를 path에 싫어 보냄
        ---
        tags:
          - Search
        parameters:
          - in: path
            type: string
            description: 검색어 문자열
        responses:
            200:
                description: 로그인 인증
                schema:
                    id: keyword
                    properties:
                        keyword:
                            type: string
                            description: 키워드 리스트, 순서대로 사용하면 됩니다
        """
        session_id = request.cookies.get('session_id')
        user_id = access_cookie(session_id)
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return Search.current_search(user.id)

class SearchPopular(Resource):
    def get(self,kw):
        """
        item 검색
        검색어를 path에 싫어 보냄
        ---
        tags:
          - Search
        parameters:
          - in: path
            type: string
            description: 검색어 문자열
        responses:
            200:
                description: 로그인 인증
                schema:
                    id: keyword
        """
        session_id = request.cookies.get('session_id')
        user_id = access_cookie(session_id)
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return Search.popular_search()

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Regist, '/regist')
api.add_resource(EventBanner, '/main/event')
api.add_resource(Mypage, '/mypage')
api.add_resource(CouponList, '/coupon')
api.add_resource(PointList, '/point')
api.add_resource(Like, '/like/<int:pid>')
api.add_resource(Cart, '/cart/<int:pid>')
api.add_resource(ImageUpload, '/event/imgup')
api.add_resource(ItemRegist, '/producer/item/regist')
api.add_resource(ProductRecommand, '/main/recommand')
api.add_resource(ProductTaste, '/main/taste')

api.add_resource(Search, '/search/<string:keyword>')
api.add_resource(SearchCurrent, '/search/current')
api.add_resource(SearchPopular, '/search/popular')

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)

