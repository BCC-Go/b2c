from app import User, app, db
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger

api = Api(app)
swagger = Swagger(app)

class Test(Resource):
    def get(self, name1):
        user = User.query.filter_by(name=name1).first()
        return {"name":user.name ,"email":user.email}
    def put(self, name1):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type = str)
        parser.add_argument("email", type = str)
        args = parser.parse_args()
        user = User(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()

        return 'success', 201

api.add_resource(Test, '/<string:name1>')

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)

