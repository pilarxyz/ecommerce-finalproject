from ecommerce.models import User, TokenBlocklist, Orders, Order_Products, Products, Product_Images, Images, Banners, Categories, Carts
from ecommerce.extensions import ma, db

class ListOrdersSchema(ma.SQLAlchemyAutoSchema):
    
    id = ma.String()
    user_name = ma.String()
    created_at = ma.String()
    user_id = ma.String()
    user_email = ma.String()
    total = ma.String()
    
    class Meta:
        ordered = True