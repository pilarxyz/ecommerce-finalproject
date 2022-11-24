from ecommerce.models import Products
from ecommerce.extensions import ma, db

class ProductSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Products
        sqla_session = db.session
        load_instance = True