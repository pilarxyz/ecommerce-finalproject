from sqlalchemy.ext.hybrid import hybrid_property

from ecommerce.extensions import db

class Carts(db.Model):
    """Basic carts model"""

    id = db.Column(db.String(36), primary_key=True, default=db.func.uuid_generate_v4())
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('carts', lazy=True))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Products', backref=db.backref('carts', lazy=True))
    quantity = db.Column(db.Integer, default=0)
    size = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "<Carts %s>" % self.name