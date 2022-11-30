from ecommerce.models import Carts
from ecommerce.extensions import ma, db

class CartSchema(ma.SQLAlchemyAutoSchema):
    
    id = ma.String()
    details = ma.String()
    price = ma.String()
    image = ma.String()
    name = ma.String()

    class Meta:
        ordered = True
        
class ShippingSchema(ma.SQLAlchemyAutoSchema):
    
    id = ma.String()
    name = ma.String()
    phone_number = ma.String()
    address = ma.String()
    city = ma.String()

    class Meta:
        ordered = True