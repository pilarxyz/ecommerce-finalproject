from ecommerce.models import Carts
from ecommerce.extensions import ma, db


class CartSchema(ma.SQLAlchemyAutoSchema):
    
    id = ma.String()
    details = ma.Dict()
    price = ma.String()
    image = ma.String()
    name = ma.String()

    class Meta:
        ordered = True
        
class ShippingSchema(ma.SQLAlchemyAutoSchema):
    
    name = ma.String()
    price = ma.Integer()

    class Meta:
        ordered = True
        
class ShippingAdressSchema(ma.SQLAlchemyAutoSchema):
    
    id = ma.String()
    name = ma.String()
    phone_number = ma.String()
    address = ma.String()
    city = ma.String()

    class Meta:
        ordered = True