from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ecommerce.api.schemas import ImageSchema
from ecommerce.models import Images, User
from ecommerce.extensions import db, ma, jwt
from ecommerce import config
# Terdapat 1 (satu) endpoint universal yang perlu dibuat oleh peserta, yaitu
# endpoint untuk mengambil atau memunculkan gambar dalam platform.
# Metode: GET
# URL: /image/{image_name.extension}
# Response: image file

class UploadImage(Resource):
    """Creation and get_all

    ---
    post:
        tags:
            - IMAGE
        summary: Upload image
        description: Upload image
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                images:
                                    type: array
                                    items: ImageSchema
    """
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()
        
        if not user:
            return {'message': 'User not found'}, 404
        
        if 'image' not in request.files:
            return {'message': 'No image found'}, 400
        
        image = request.files['image']
        if image.filename == '':
            return {'message': 'No image found'}, 400
        
        if image:
            image = Images(
                image_url=image.filename,
                user_id=user_id
            )
            db.session.add(image)
            db.session.commit()
            
            return jsonify(
                {
                    'data': ImageSchema().dump(image)
                }
            )

class GetImage(Resource):
    """Creation and get_all

    ---
    get:
        tags:
            - IMAGE
        summary: Get image
        description: Get image
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                images:
                                    type: array
                                    items: ImageSchema
    """
    
    def get(self, image_name):
        image = db.session.execute(
            f"""
            SELECT id, name, CONCAT('{config.BACKEND_HOST}/', image_url) AS image
            FROM images
            """
        ).fetchall()
        
        if not image:
            return {'message': 'Image not found'}, 404
        
        return jsonify(
            {
                'data': ImageSchema(many=True).dump(image)
            }
        )