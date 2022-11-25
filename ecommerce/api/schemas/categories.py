from ecommerce.models import Categories
from ecommerce.models import Images
from ecommerce.extensions import ma, db

class CategoryImageSchema(ma.SQLAlchemyAutoSchema):
    id = ma.String()
    title = ma.String()
    image = ma.String()

    class Meta:
        sqla_session = db.session
        include_fk = True
        include_relationships = True