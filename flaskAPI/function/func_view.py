from ast import keyword
from audioop import ratecv
from model import *
from function.func_user import item_to_dict, all_item
from random import randint, shuffle
    
def product_preview(item, n):
    result = []
    for i in range(n):
        res = item_to_dict(item[i][0])
        res.update(item_to_dict(item[i][1]))
        result.append(ProductFunc.discount(res,item[i][0].id))
    return result

class CategoryView():
    def show_category_all():
        category = CategoryLarge.query.all()
        return all_item(category,len(category))
    
    def show_category_mid(category_large_id):
        category = CategoryMid.query.filter_by(category_large_id=category_large_id).all()
        return all_item(category,len(category))
    
    # def show_item(category_mid_id):
    #     category = CategorySmall.query.filter_by(category_mid_id=category_mid_id).all()
    #     product = Product.query.filter_by(category_mid_id=category_mid_id).all()
    #     res=[]
    #     for i in range(len(category)-1):
    #         res.append(category[i].id)

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
        
    def show_detail_product(product_id):
        items = db.session.query(Product,ProductDetail).filter(Product.id == ProductDetail.product_id, Product.id == product_id).first()
        return product_preview(items, 1)

    def find_small_category(category_mid_id):
        cate_list = CategorySmall.query.filter_by(category_mid_id = category_mid_id).all()
        return [cate_list[randint(1,len(cate_list)-1)].id, cate_list[randint(1,len(cate_list)-1)].id]

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
        return product_preview(item,num)

    def discount(res, id):
        discount = Discount.query.filter_by(product_id = id).first()
        if discount == []:
            return res
        else:
            if discount.expire() == 0:
                db.session.delete(discount)
                db.session.commit()
            if discount.expire() == 1:
                item = Product.query.filter_by(id = id).first()
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
        


class Search():
    def search_key(id,kw): # 유저 검색
        Search.manage(id, kw)
        search = '%%{}%%'.format(kw)
        items = db.session.query(Product,ProductDetail).filter(Product.id == ProductDetail.product_id, Product.name.ilike(search)).all()
        return product_preview(items, len(items))

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