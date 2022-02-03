from flask import make_response, jsonify, request
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger
from flask_cors import CORS
from model import app, db, User
from function.func_user import UserFunction, access_cookie
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
                        
        """

        session_id = request.headers['Session']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.recommand(user.id,12,'r')

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
        return UserFunction.recommand(user.id,12,'t')

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


class ImageUpload(Resource):
    def post(self):
        """
        이벤트 이미지 업로드
        ---
        tags:
          - ImageUpload
        parameters:
          - in: fromData
            name: file
            type: file
            requirement: true
          - in: body
            name: expire
            type: string
            description: 'Example : 2022-02-02 22:22:22'
        responses:
            200:
                description: upload success

        """
        f = request.files['file']
        data = request.get_json()
        Image.upload(f,data['expire'])

        return "success"

    
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Regist, '/regist')
api.add_resource(EventBanner, '/main/event')
api.add_resource(ProductRecommand, '/main/recommand')
api.add_resource(ProductTaste, '/main/taste')
api.add_resource(Mypage, '/mypage')
api.add_resource(CouponList, '/coupon')
api.add_resource(ImageUpload, '/imgup')

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)

