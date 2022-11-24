from ecommerce.models import User
from ecommerce.extensions import ma, db


class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password",)
