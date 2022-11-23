from sqlalchemy.ext.hybrid import hybrid_property

from ecommerce.extensions import db

class Product_Images (db.Model):
    """Basic product_images model"""

    id = db.Column(db.String(36), primary_key=True, default=db.func.uuid_generate_v4())
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Products', backref=db.backref('product_images', lazy=True))
    image_id = db.Column(db.String(36), db.ForeignKey('images.id'), nullable=False)
    image = db.relationship('Images', backref=db.backref('product_images', lazy=True))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "<Product_Images %s>" % self.name