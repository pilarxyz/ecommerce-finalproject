from sqlalchemy.ext.hybrid import hybrid_property

from ecommerce.extensions import db

class Categories(db.Model):
    """Basic categories model"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return "<Categories %s>" % self.name
    
    