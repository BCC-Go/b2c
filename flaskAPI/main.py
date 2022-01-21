from app import *
from session import Session, dbs
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger
from datetime import timedelta, datetime

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
    
        resp = make_response(jsonify({'status': 'success'}))
        resp.set_cookie('session_id',str(session.id), expires=expires)
        return resp

class Logout(Resource):
    def put(self):
        session_id = request.cookies.get('session_id')
        dbs.session.delete(Session.query.filter_by(id=session_id).first())
        dbs.session.commit()
        response = make_response('logout')
        response.set_cookie('session_id', expires=0)
        return response


api.add_resource(Login, '/Login')
api.add_resource(Logout, '/Logout')

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)

