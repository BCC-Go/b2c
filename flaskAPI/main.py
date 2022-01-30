from app import *
from session import Session, dbs
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger
from datetime import timedelta, datetime
from flask_cors import CORS
from func_user import UserFunction, access_cookie

CORS(app,supports_credentials=True)
api = Api(app)
swagger = Swagger(app)
app.config['CORS_HEADERS'] = 'Content-Type'
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
            name: loginId
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
        dbs.session.delete(Session.query.filter_by(id=session_id).first())
        dbs.session.commit()
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
          - ProductRecommand
        responses:
            0:
                description: 로그인 안한 상태 int형으로 0 리턴
            200:
                description: 로그인 인증
        """
        session_id = request.headers['Session']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        recom = UserRecommand.query.filter_by(user_id=user.id).first()
        return UserFunction.recommand(recom,12)

class ProductTaste(Resource):
    def get(self):
        """
        메인페이지 추천상품
        로그인 안했으면 로그인을 하면 더 자세한 상품을 볼 수 있다고 표시
        ---
        tags:
          - ProductTaste
        responses:
            0:
                description: 로그인 안한 상태 int형으로 0 리턴
            200:
                description: 로그인 인증
        """
        session_id = request.cookies.get('session_id')
        user_id = access_cookie(session_id)
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        recom = UserRecommand.query.filter_by(user_id=user.id).first()
        return UserFunction.recommand(recom,12)

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Regist, '/regist')
api.add_resource(EventBanner, '/main/event')
api.add_resource(ProductRecommand, '/main/recommand')
api.add_resource(ProductTaste, '/main/taste')

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)

