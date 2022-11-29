from ecommerce.models import Carts
from ecommerce.extensions import ma, db

class CartSchema(ma.SQLAlchemyAutoSchema):
    
    id = ma.String()
    user_id = ma.String()
    product_id = ma.String()
    quantity = ma.String()

    class Meta:
        ordered = True