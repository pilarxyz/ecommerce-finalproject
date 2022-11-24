from sqlalchemy.ext.hybrid import hybrid_property

from ecommerce.extensions import db

class Categories(db.Model):
    """Basic categories model"""

    id = db.Column(db.String(36), primary_key=True, default=db.func.uuid_generate_v4())
    title = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return "<Categories %s>" % self.name
    
    