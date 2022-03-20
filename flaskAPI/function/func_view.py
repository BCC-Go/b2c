from datetime import timedelta
from model import *
from random import randint, shuffle
item_to_dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

def all_item(item, n):
    result = []
    for i in range(n):
        result.append(item_to_dict(item[i]))
    return result

def product_preview(item, n, uid):
    result = []
    for i in range(n):
        res = item_to_dict(item[i][0])
        res.update(item_to_dict(item[i][1]))
        result.append(ProductFunc.discount(res,item[i][0].id, uid))
    return result

class CategoryView():
    def show_category_all():
        category = CategoryLarge.query.all()
        return all_item(category,len(category))
    
    def show_category_mid(category_large_id):
        category = CategoryMid.query.filter_by(category_large_id=category_large_id).all()
        return all_item(category,len(category))

class ProductFunc():
    def regist_product(user, category_name, name, price, image, brand, summary, detail):
        if user.type != 1:
            return 0
        cate = CategorySmall.query.filter_by(name = category_name).first()
        new = Product(category_small_id = cate.id, name = name, price = price, image = image, brand = brand, avg_star = 0, regist_time = koreaNow())
        db.session.add(new)
        db.session.commit()
        new_detail = ProductDetail(product_id = new.id, summary = summary, detail = detail)
        db.session.add(new_detail)
        db.session.commit()
        return '상품등록 성공', 200 
        
    def show_detail_product(uid, product_id):
        items = db.session.query(Product,ProductDetail).filter(Product.id == ProductDetail.product_id, Product.id == product_id).first()
        res = item_to_dict(items[0])
        res.update(item_to_dict(items[1]))
        ProductFunc.discount(res,items[0].id, uid.id)
        return res

    def find_small_category(category_mid_id):
        cate_list = CategorySmall.query.filter_by(category_mid_id = category_mid_id).all()
        cate = [cate_list[randint(0,len(cate_list)-1)].id]
        cate_list.remove(cate_list[cate[0]-1])
        cate.append(cate_list[randint(0,len(cate_list)-1)].id)
        return cate

    def recommand(id,num,type):
        if type == 'r':
            recom = UserRecommand.query.filter_by(user_id=id).first()
            reco = ProductFunc.find_small_category(recom.category_mid_id)
        elif type == 't':
            recom = UserTaste.query.filter_by(user_id=id).first()
            reco = ProductFunc.find_small_category(recom.category_mid_id)
        else:
            reco = ProductFunc.find_small_category(type)
        items1 = db.session.query(Product,ProductDetail).filter(Product.id == ProductDetail.product_id, Product.category_small_id == reco[0]).all()
        items2 = db.session.query(Product,ProductDetail).filter(Product.id == ProductDetail.product_id, Product.category_small_id == reco[1]).all()
        #items1 = Product.query.filter_by(category_small_id = reco[0]).all()
        #items2 = Product.query.filter_by(category_small_id = reco[1]).all()
        item = items1+items2
        shuffle(item)
        if num == 0 or num > len(item):
            num = len(item)
        return product_preview(item,num, id)

    def discount(res, pid, uid):
        discount = Discount.query.filter_by(product_id = pid).first()
        like2 = Like.query.filter_by(user_id = uid, product_id = pid).first()
        if not like2:
            res['like'] = 0
        else:
            res['like'] = 1
        
        if not discount:
            return res
        else:
            if discount.expire() == 0:
                db.session.delete(discount)
                db.session.commit()
            if discount.expire() == 1:
                item = Product.query.filter_by(id = pid).first()
                if discount.rate < 100:
                    amount = item.price * (100-discount.rate) / 100
                    rate = str(discount.rate)+'%'
                else:
                    amount = item.price - discount.rate 
                    rate = str(discount.rate)+'원'
                res['rate'] = rate
                res['amount'] = amount
                return res
            return res

    def buyItem(user,pid,point,count):
        item = Product.query.filter_by(id = pid).first()
        discount = Discount.query.filter_by(product_id = pid).first()
        if discount == []:
            price = item.price * count - point
        else:
            if discount.rate < 100:
                price = count * (item.price * (100-discount.rate) / 100) - point
            else:
                price = count * (item.price - discount.rate) - point
        content = "{}".format('point : ' + str(point) + '을(를) 사용하여 ',item.name, ' 상품을 구매')
        pp = Point(user_id = user.id,point = 0 - point, content = content)
        db.session.add(pp)
        db.session.commit()
        return price
    
    def newItem(uid):
        item = Product.query.filter(Product.regist_time > koreaNow() - timedelta(days = 7)).order_by(Product.id.desc()).all()
        return product_preview(item, len(item), uid)


class Search():
    def search_key(id,kw): # 유저 검색
        Search.manage(id, kw)
        search = '%%{}%%'.format(kw)
        items = db.session.query(Product,ProductDetail).filter(Product.id == ProductDetail.product_id, Product.name.ilike(search)).all()
        return product_preview(items, len(items), id)

    # 최근 검색어 10개 이하로 관리하기
    def manage(id, kw):
        search = SearchUser(user_id = id, keyword = kw)
        sea = SearchUser.query.filter_by(user_id = id).all()
        key = SearchPopular.query.filter_by(keyword = kw).first()
        if key == []:
            key = SearchPopular(keyword = kw, count = 1)
            db.session.add(key)
        else:
            key.search()
        if len(sea) == 10:
            db.session.delete(sea[0])
        db.session.add(search)
        db.session.commit()

    def current_search(id):
        sea = db.session.query(SearchUser.keyword).filter_by(user_id = id).all()
        sea.reverse()
        return sea

    def popular_search():
        key = db.session.query(SearchPopular.keyword).order_by(SearchPopular.count.desc())
        if len(key) >= 10:
            return key[:10]
        else:
            return key
