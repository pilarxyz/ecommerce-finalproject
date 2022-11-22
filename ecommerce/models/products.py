from sqlalchemy.ext.hybrid import hybrid_property

from ecommerce.extensions import db

class Products(db.Model):
    """Basic products model"""

    id = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.String(80), unique=True, nullable=False)
    condition = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Categories', backref=db.backref('products', lazy=True))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return "<Products %s>" % self.name