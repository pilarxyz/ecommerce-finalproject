from sqlalchemy.ext.hybrid import hybrid_property

from ecommerce.extensions import db

class Orders(db.Model):
    """Basic orders model"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    status = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=True, nullable=False)
    city = db.Column(db.String(80), unique=True, nullable=False)
    shipping_price = db.Column(db.String(80), unique=True, nullable=False)
    shipping_method = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "<Orders %s>" % self.name