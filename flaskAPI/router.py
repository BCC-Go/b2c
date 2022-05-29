from flask import make_response, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_restful.reqparse import RequestParser
from flasgger import Swagger
from flask_cors import CORS
from model import app, db, User
from function.func_user import UserFunction, access_cookie
from function.func_view import CategoryView, ProductFunc
from function.func_img import Image
from werkzeug.datastructures import FileStorage

CORS(app,supports_credentials=True)
api = Api(app)
swagger = Swagger(app)

# 유저 관련
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
        session = UserFunction.login(data['login_id'],data['password'])
        resp = make_response(jsonify({'session_id': session}))

        if session == 0:
            return resp
        return resp

class Logout(Resource):
    def post(self):
        """
        delete cookie 
        ---
        tags:
          - Logout
        responses:
            200:
                description: cookie is expired
        """
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        UserFunction.logout(user.id)
        return 200
        
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
        session_id = request.headers['session_id']
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
        session_id = request.headers['session_id']
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
        session_id = request.headers['session_id']
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
          - in: form
            name: file
            type: string
        responses:
            200:
                description: upload success

        """
        f = request.files['file']
        Image.upload(f)

        return "success"

# 상품 유저 관련
class Like(Resource):
    def get(self,pid):
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
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.list_like(user.id)

    def post(self,pid):
        """
        상품에 좋아요 하기
        ---
        tags:
          - Like
        parameters:
          - in: body
            name: pid
            type: int
            requirement: true
        responses:
            200:
                description: 상품 좋아요 성공
        """
        session_id = request.headers['session_id']
        data = request.get_json()
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.add_like(user.id,data['pid'])

    def delete(self,pid):
        """
        상품에 좋아요 취소
        ---
        tags:
          - Like
        parameters:
          - in: path
            name: pid
            type: int
            requirement: true
        responses:
            200:
                description: 상품 좋아요 취소 성공
        """
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.delete_like(user.id,pid)

class Cart(Resource):
    def get(self,pid):
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
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.list_cart(user.id)

    def post(self,pid):
        """
        상품에 좋아요 하기
        ---
        tags:
          - Cart
        parameters:
          - in: body
            name: pid
            type: int
            requirement: true
        responses:
            200:
                description: 상품 좋아요 성공
        """
        session_id = request.headers['session_id']
        data = request.get_json()
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.add_cart(user.id,data['pid'])

    def delete(self,pid):
        """
        상품에 좋아요 취소
        ---
        tags:
          - Cart
        parameters:
          - in: body
            name: pid
            type: int
            requirement: true
        responses:
            200:
                description: 상품 좋아요 취소 성공
        """
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.delete_cart(user.id,pid)

# 상품 관련
class ItemRegist(Resource):
    def post(self):
        """
        상품 추가 하기
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
          - in: form
            name: file
            type: string
        responses:
            200:
                description: 상품 좋아요 성공
        """
        f = request.files['file']
        session_id = request.headers['session_id']
        data = request.get_json()
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        if user.type == 1:
          return ProductFunc.regist_product(user, data['category_name'], data['name'], data['price'], f, data['brand'], data['summary'], data['detail'])
        else:
          return "No auth",500

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
                        rate:
                            type: string
                            description: 비율이면 XX%, 금액이면 XX원 (할인하는 상품만 존재)
                        amount:
                            type: int
                            description: 상품 최종 가격 (할인하는 상품만 존재)
                        like:
                            type: int
                            description: 좋아요한 상품 1, 아닌 상품 0
        """

        session_id = request.headers['session_id']
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
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return ProductFunc.recommand(user.id,12,'t')

class NewProduct(Resource):
    def get(self):
        """
        신상품 페이지
        ---
        tags:
          - Product View
        responses:
            200:
                description: 로그인 인증
                schema:
                    id: product view
        """
        session_id = request.cookies.get('session_id')
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return ProductFunc.newItem(user.id)

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
        user_id = access_cookie(session_id[11:])
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
        user_id = access_cookie(session_id[11:])
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
        responses:
            200:
                description: 로그인 인증
                schema:
                    id: keyword
        """
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return Search.popular_search()

class ItemDetail(Resource):
    def get(self,pid):
        """
        상품 눌렀을 때 상세 화면
        ---
        tags:
          - Product Detail
        parameters:
          - in: body
            name: pid
            type: int
            requirement: true
        responses:
            200:
                description: 상품 상세 보기
                schema:
                    id: product view
        """
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return ProductFunc.show_detail_product(user, pid)

class BigCateView(Resource):
    def get(self):
        """
        최상위 카테고리 보기
        ---
        tags:
          - CategoryView
        responses:
            200:
                description: 카테고리 정보 리턴
                schema:
                    Properties:
                        id:
                            type: int
                            description: 고유 번호, 클릭할 때 전송 용도
                        name:
                            type: string
                            description: 카테고리 이름
                        image:
                            type: string
                            description: 카테고리 이미지 url
        """
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        return CategoryView.show_category_all()

class MidCateView(Resource):
    def get(self,cid):
        """
        중간 카테고리 보기
        ---
        tags:
          - CategoryView
        parameters:
          - in: path
            name: cid
            type: string
            description: 카테고리 라지 고유 번호
        responses:
            200:
                description: 중간 카테고리 정보
                schema:
                    Properties:
                        id:
                            type: int
                            description: 고유 번호, 클릭할 때 전송 용도
                        name:
                            type: string
                            description: 카테고리 이름
        """
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        return CategoryView.show_category_mid(cid)

class ShowCateItem(Resource):
    def get(self,cid):
        """
        중간 카테고리 상품 보기
        ---
        tags:
          - CategoryView
        parameters:
          - in: path
            name: cid
            type: string
            description: 카테고리 미드 고유 번호
        responses:
            200:
                description: 중간 카테고리 관련 상품 보기
                schema:
                    id: product view
        """
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        user = User.query.filter_by(id = user_id).first()
        return ProductFunc.recommand(user.id,0,cid)

class BuyItem(Resource):
    def post(self):
        """
        상품 구매 요청
        ---
        tags:
          - buy product
        parameters:
          - in: body
            name: product_id
            type: int
            description: 상품 고유 번호
          - in: body
            name: point
            type: int
            description: 사용할 포인트
          - in: body
            name: count
            type: int
            description: 구매 할 수
        """
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        data = request.get_json()
        user = User.query.filter_by(id = user_id).first()
        return ProductFunc.buyItem(user,data['product_id'],data['point'],data['count'])

class ReviewLoad(Resource):
    def get(self,pid):
        """
        상품에 대한 리뷰 내용
        ---
        tags:
          - Review
        parameters:
          - in: path
            type: int
            description: 상품 고유 번호
        responses:
            200:
                description: 상품에 대한 리뷰 읽어오기
                schema:
                    id: review_view
                    properties:
                        name:
                            type: string
                            description: 유저 이름
                        content:
                            type: string
                            description: 리뷰 내용
                        image:
                            type: string    
                            description: 리뷰 이미지 url
                        star:
                            type: float
                            description: 유저가 준 별점
                        write_time:
                            type: string
                            description: 리뷰 작성 날짜 및 시간
        """    
        return UserFunction.load_review(pid)

class ReviewRegist(Resource):
    def post(self):
        """
        상품에 리뷰 등록하기
        ---
        tags:
          - Review
        parameters:
          - in: body
            name: product_id
            type: int
            description: 상품 고유 번호
          - in: body
            name: content
            type: string
            description: 유저가 쓴 리뷰 내용
          - in: body
            name: star
            type: float
            description: 유저가 준 별점
          - in: file
            name: image
            type: file
            description: 리뷰 이미지
        responses:
            200:
                description: 상품에 리뷰 등록 성공
        """    
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        data = request.get_json()
        user = User.query.filter_by(id = user_id).first()
        if 'file' not in request.files:
            return UserFunction.regist_review(user.id,data['product_id'],data['content'],data['star'])
        f = request.files['file']
        print(f)
        return UserFunction.regist_review_img(user.id,data['product_id'],data['content'],f,data['star'])

class QuestionLoad(Resource):
    def get(self,pid):
        """
        상품에 대한 리뷰 내용
        ---
        tags:
          - Question
        parameters:
          - in: path
            type: int
            description: 상품 고유 번호
        responses:
            200:
                description: 상품에 대한 질문 읽어오기
                schema:
                    id: question_view
                    properties:
                        question_title:
                            type: string
                            description: 질문 제목
                        question_content:
                            type: string
                            description: 질문 내용
                        question_hashtag:
                            type: string    
                            description: 질문 hashtag
                        question_write_time:
                            type: string
                            description: 질문 등록 시잔
                        name:
                            type: string
                            description: 답변자 이름
                        answer_content:
                            type: string
                            description: 답변 내용
                        answer_write_time:
                            type: string
                            description: 답변 등록 시잔
        """    
        return UserFunction.load_question(pid)

class QuestionRegist(Resource):
    def post(self):
        """
        상품에 질문 등록하기
        ---
        tags:
          - Question
        parameters:
          - in: body
            name: product_id
            type: int
            description: 상품 고유 번호
          - in: body
            name: title
            type: string
            description: 질문 제목
          - in: body
            name: content
            type: string
            description: 질문 내용
          - in: body
            name: content
            type: string
            description: 질문 내용
          - in: body
            name: hashtag
            type: string
            description: hashtag
        responses:
            200:
                description: 상품에 질문 등록 성공
        """    
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        data = request.get_json()
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.regist_question(user.id,data['product_id'],data['title'],data['content'],data['hashtag'])

class AnswerRegist(Resource):
    def post(self):
        """
        상품에 질문 등록하기
        ---
        tags:
          - Question
        parameters:
          - in: body
            name: product_id
            type: int
            description: 상품 고유 번호
          - in: body
            name: title
            type: string
            description: 질문 제목
          - in: body
            name: content
            type: string
            description: 질문 내용
          - in: body
            name: content
            type: string
            description: 질문 내용
          - in: body
            name: hashtag
            type: string
            description: hashtag
        responses:
            200:
                description: 상품에 질문 등록 성공
        """    
        session_id = request.headers['session_id']
        user_id = access_cookie(session_id[11:])
        if 0 == user_id:
            return 0 # no login
        data = request.get_json()
        user = User.query.filter_by(id = user_id).first()
        return UserFunction.regist_question(user.id,data['product_id'],data['title'],data['content'],data['hashtag'])

class ImageUp(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('images', FileStorage, 'images', 'appand')
        args = parser.parse_args()
        img = args['images']
        img_name = args['imgName']
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        img_path = os.path.join(root_dir, 'static', 'images', img_name)
        with open(img_path, 'wb') as fh:
            fh.write(img.read())
        resp = make_response(img_name)
        resp.content_type = 'text/plain'
        return resp


api.add_resource(ImageUp, '/uplo')

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
api.add_resource(NewProduct, '/product/new')

api.add_resource(Search, '/search/<string:keyword>')
api.add_resource(SearchCurrent, '/search/current')
api.add_resource(SearchPopular, '/search/popular')
api.add_resource(ItemDetail, '/detail/<int:pid>')

api.add_resource(BigCateView, '/category/large')
api.add_resource(MidCateView, '/category/mid/<int:cid>')
api.add_resource(ShowCateItem, '/category/item/<int:cid>')

api.add_resource(ReviewLoad, '/product/review/<int:pid>')
api.add_resource(ReviewRegist, '/product/review/regist')
api.add_resource(QuestionLoad, '/product/question/<int:pid>')
api.add_resource(QuestionRegist, '/product/question/regist')
api.add_resource(AnswerRegist, '/product/question/answer/regist')



if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)

