from app import *
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger
from datetime import timedelta

api = Api(app)
swagger = Swagger(app)

class Login(Resource):

#    def get(self, name1):

 #       user = User.query.filter_by(name=name1).first()
  #      return {"name":user.name ,"email":user.email}
    def put(self,name1):
        parser = reqparse.RequestParser()
        parser.add_argument("loginId", type = str)
        parser.add_argument("password", type = str)
        args = parser.parse_args()
        user = User.query.filter_by(loginId=args['loginId']).first()
        if user.password == args['password']:
            session['userid'] = user.id
            return {'session_id':session['userid']}
        #db.session.add(user)
        #db.session.commit()

        return "id와 비밀번호가 일치하지 않습니다.", 201

class Test2(Resource):
    def get(self):
        if 'userid' in session:
            return 'success', 201
        return "f"

        #parser = reqparse.RequestParser()
        #parser.add_argument("session_id", type = str)
        #args = parser.parse_args()

       # user = User.query.filter_by(id=int(seid)).first()
       # return {"name":user.name ,"consumption":user.rank.grade}


api.add_resource(Login, '/<string:name1>')
api.add_resource(Test2, '/test')

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)

