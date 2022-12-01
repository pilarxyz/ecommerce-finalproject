from ecommerce.models import Categories
from ecommerce.extensions import ma, db


class CategoriesSchema(ma.SQLAlchemyAutoSchema):
    
    id = ma.String()
    title = ma.String()
    
    class Meta:
        ordered = True