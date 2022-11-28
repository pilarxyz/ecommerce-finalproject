from ecommerce.models import Banners, Categories, Images, Products, Product_Images
from ecommerce.extensions import ma, db

class BannerSchema(ma.SQLAlchemyAutoSchema):
    
    id = ma.String()
    image = ma.String()
    title = ma.String()
    
    class Meta:
        ordered = True
    
class CategoryImageSchema(ma.SQLAlchemyAutoSchema):
    
    id = ma.String()
    image = ma.String()
    title = ma.String()
    
    class Meta:
        ordered = True

