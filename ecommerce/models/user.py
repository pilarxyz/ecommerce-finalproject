from sqlalchemy.ext.hybrid import hybrid_property

from ecommerce.extensions import db, pwd_context

class User(db.Model):
    """Basic users model"""

    id = db.Column(db.String(36), primary_key=True, default=db.func.uuid_generate_v4())
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    phone_number = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return "<User %s>" % self.username