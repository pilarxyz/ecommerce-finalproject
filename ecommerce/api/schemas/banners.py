from ecommerce.models import Banners
from ecommerce.extensions import ma, db

class BannerSchema(ma.SQLAlchemyAutoSchema):
    
    id = ma.String()
    image = ma.String()
    title = ma.String()
        
    class Meta:
        sqla_session = db.session