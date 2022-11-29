from ecommerce.models import Products, Product_Images, Images, Categories
from ecommerce.extensions import ma, db

class ProductSchema(ma.SQLAlchemyAutoSchema):
    
    id = ma.String()
    title = ma.String()
    price = ma.String()
    image = ma.String()   
    
    class Meta:
        ordered = True
        
class ProductDetailSchema(ma.SQLAlchemyAutoSchema):
        
    id = ma.String()
    title = ma.String()
    size = ma.String()
    product_detail = ma.String()
    price = ma.String()
    image_url = ma.String()
    condition = ma.String()
    category_id = ma.String()
    category_name = ma.String()

    class Meta:
        ordered = True
        
