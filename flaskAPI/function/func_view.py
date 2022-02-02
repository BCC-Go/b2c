from model import *
from function.func_user import item_to_dict, all_item

def show_detail_product(product_id):
        product = Product.query.filter_by(id = product_id).first()
        result = item_to_dict(product_id)
        result['summary'] = product.product_detail.summary
        result['detail'] = product.product_detail.detail
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

