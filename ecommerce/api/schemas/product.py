from ecommerce.models import Products, Product_Images, Images, Categories
from ecommerce.extensions import ma, db

class ProductSchema(ma.SQLAlchemyAutoSchema):
    
    id = ma.String()
    title = ma.String()
    price = ma.String()
    image = ma.String()
    category = ma.String()
    description = ma.String()
    condition = ma.String()
    
    class Meta:
        ordered = True
        
class ProductDetailSchema(ma.SQLAlchemyAutoSchema):
        
    id = ma.String()
    title = ma.String()
    size = ma.String()
    product_detail = ma.String()
    price = ma.String()
    images_url = ma.String()
    condition = ma.String()
    category_id = ma.String()
    category_name = ma.String()

    class Meta:
        ordered = True
        
