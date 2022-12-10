from sqlalchemy.ext.hybrid import hybrid_property

from ecommerce.extensions import db

class Orders(db.Model):
    """Basic orders model"""

    id = db.Column(db.String(36), primary_key=True, default=db.func.uuid_generate_v4())
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    status = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    address_name = db.Column(db.String(80), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    phone_number = db.Column(db.String(80), nullable=True)
    shipping_price = db.Column(db.String(80), nullable=False)
    shipping_method = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "<Orders %s>" % self.name