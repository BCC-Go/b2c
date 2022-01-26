from app import *
from session import Session, dbs
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger
from datetime import timedelta, datetime
from flask_cors import CORS

CORS(app)
api = Api(app)
swagger = Swagger(app)

# session 만료
def expire(expires):
    now = datetime.now()
    diff = str(expires - now)
    if diff[4] == '-': # 현재시간이 만료를 지났으면 diff = expires로 설정되어 2022- ~~로 나옴
        return 0
    return 1

def access_cookie(session_id,expires):
    # session_id = request.cookies.get('session_id')
    # expires = request.cookies.get('Expires')
    session = Session.query.filter_by(id=session_id).first()
    if session.id & expire(expires):
        return session.user_id # success
    dbs.session.delete(session)
    dbs.session.commit()
    return 0 # fail

class Login(Resource):
    def put(self):
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
        parser = reqparse.RequestParser()
        parser.add_argument("loginId", type = str)
        parser.add_argument("password", type = str)
        args = parser.parse_args()
        user = User.query.filter_by(loginId=args['loginId']).first()
        if user.password == args['password']:
            session = Session(user_id = user.id)
            dbs.session.add(session)
            dbs.session.commit()

        expires_in = timedelta(hours=1)  # cookie 기간
        expires = datetime.now() + expires_in
        print(expires)
        resp = make_response(jsonify({'session_id': str(session.id), 'expire': str(expires)}))

        resp = make_response(jsonify({'status': 'success'}))
        resp.set_cookie('session_id',str(session.id), expires=expires)
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
        response.set_cookie('session_id', expires=0)
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
            responses:
            200:
                description: 성공하면 로그인 페이지로 이동
        """
        data = request.get_json()
        user = User(rank_id = 1, login_id = data['login_id'], password = data['password'], name = data['name'], phone = data['phone'], sex = int(data['sex']), birth = data['birth'], consumption = 0, address = data['address'], type = 0)
        db.session.add(user)
        db.session.commit()
        return "",200

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
        session_id = request.cookies.get('session_id')
        expires = request.cookies.get('Expires')
        user_id = access_cookie(session_id,expires)
        if not user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()

        return "success"
        # todo 이걸로 small category id 여러개 골라서 필터링 함수 잘 짜야할 듯
        # user.user_recommand.category_mid_id 

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Regist, '/regist')
api.add_resource(EventBanner, '/main/event')
api.add_resource(ProductRecommand, '/main/recommand')

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)

