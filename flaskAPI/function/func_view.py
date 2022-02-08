from model import *
from function.func_user import item_to_dict, all_item
from random import randint, shuffle
    
def product_preview(item, n):
    result = []
    for i in range(n):
        res = item_to_dict(item[i][0])
        res.update(item_to_dict(item[i][1]))
        result.append(res)
    return result

class CategoryView():
    def show_category_all():
        category = CategoryLarge.query.all()
        return all_item(category,len(category))
    
    def show_category_mid(category_large_id):
        category = CategoryMid.query.filter_by(category_large_id=category_large_id).all()
        return all_item(category,len(category))
    
    def show_item(category_mid_id):
        category = CategorySmall.query.filter_by(category_mid_id=category_mid_id).all()
        product = Product.query.filter_by(category_mid_id=category_mid_id).all()
        res=[]
        for i in range(len(category)-1):
            res.append(category[i].id)

class ProductFunc():
    def regist_product(user, category_name, name, price, image, brand):
        if user.type != 1:
            return 0
        cate = CategorySmall.query.filter_by(name = category_name).first()
        new = Product(category_small_id = cate.id, name = name, price = price, image = image, brand = brand, avg_star = 0, regist_time = koreaNow())
        db.session.add(new)
        db.session.commit()
        return '상품등록 성공', 200 

    def search_key(kw):
        search = '%%{}%%'.format(kw)
        items = db.session.query(Product,ProductDetail).filter(Product.id == ProductDetail.product_id, Product.name.ilike(search)).all()
        return product_preview(items, len(items))
        
    def show_detail_product(product_id):
        items = db.session.query(Product,ProductDetail).filter(Product.id == ProductDetail.product_id, Product.id == product_id).first()
        result = item_to_dict(items[0])
        result.update(items[1])
        return result

    def find_small_category(category_mid_id):
        cate_list = CategorySmall.query.filter_by(category_mid_id = category_mid_id).all()
        return [cate_list[randint(1,len(cate_list)-1)].id, cate_list[randint(1,len(cate_list)-1)].id]

    def recommand(id,num,type):
        if type == 'r':
            recom = UserRecommand.query.filter_by(user_id=id).first()
        else:
            recom = UserRecommand.query.filter_by(user_id=id).first()
        reco = ProductFunc.find_small_category(recom.category_mid_id)
        items1 = db.session.query(Product,ProductDetail).filter(Product.id == ProductDetail.product_id, Product.category_small_id == reco[0]).all()
        items2 = db.session.query(Product,ProductDetail).filter(Product.id == ProductDetail.product_id, Product.category_small_id == reco[1]).all()
        #items1 = Product.query.filter_by(category_small_id = reco[0]).all()
        #items2 = Product.query.filter_by(category_small_id = reco[1]).all()
        item = items1+items2
        shuffle(item)
        if num == 0 or num > len(item):
            num = len(item)
        return product_preview(item,num)