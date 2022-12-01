from ecommerce.models import User
from ecommerce.extensions import ma, db


class UserSchema(ma.SQLAlchemyAutoSchema):

    name = ma.String()
    email = ma.String()
    phone_number = ma.String()
    balance = ma.String()
    
    class Meta:
        ordered = True

class ChangeShippingSchema(ma.SQLAlchemyAutoSchema):

    name = ma.String()
    phone_number = ma.String()
    address = ma.String()
    city = ma.String()
    
    class Meta:
        ordered = True
        
class GetBalanceSchema(ma.SQLAlchemyAutoSchema):

    balance = ma.String()
    
    class Meta:
        ordered = True