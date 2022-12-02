from ecommerce.models import Images
from ecommerce.extensions import ma, db

class ImageSchema(ma.SQLAlchemyAutoSchema):
        
        id = ma.String()
        name = ma.String()
        image = ma.String()
        
        class Meta:
            ordered = True