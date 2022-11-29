from ecommerce.models import Products, Product_Images, Images
from ecommerce.extensions import ma, db

class ProductSchema(ma.SQLAlchemyAutoSchema):
    
    id = ma.String()
    title = ma.String()
    price = ma.String()
    condition = ma.String()
    image = ma.String()   
    
    class Meta:
        ordered = True