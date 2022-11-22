from sqlalchemy.ext.hybrid import hybrid_property

from ecommerce.extensions import db

class Banners(db.Model):
    """Basic banners model"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    image = db.relationship('Images', backref=db.backref('banner', lazy=True))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return "<Banners %s>" % self.name
    
    