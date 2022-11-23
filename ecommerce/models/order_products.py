from sqlalchemy.ext.hybrid import hybrid_property


from ecommerce.extensions import db

class Order_Products (db.Model):
    """Basic order_products model"""
    
    id = db.Column(db.String(36), primary_key=True, default=db.func.uuid_generate_v4())
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    order = db.relationship('Orders', backref=db.backref('order_products', lazy=True))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Products', backref=db.backref('order_products', lazy=True))
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(80), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return "<Order_Products %s>" % self.name