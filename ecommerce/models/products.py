from sqlalchemy.ext.hybrid import hybrid_property

from ecommerce.extensions import db

class Products(db.Model):
    """Basic products model"""

    id = db.Column(db.String(36), primary_key=True, default=db.func.uuid_generate_v4())
    title = db.Column(db.String(80), nullable=False)
    product_detail = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=True)
    size = db.Column(db.String(80), nullable=False)
    condition = db.Column(db.String(80), nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Categories', backref=db.backref('products', lazy=True))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return "<Products %s>" % self.name