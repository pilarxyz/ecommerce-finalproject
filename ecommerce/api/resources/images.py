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
# create in folder static/images
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'User not found'}, 404
        if not request.files:
            return {'message': 'No file found'}, 400
        file = request.files['file']
        if not file:
            return {'message': 'No file found'}, 400
        if file.filename == '':
            return {'message': 'No file found'}, 400
        if not file.filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS:
            return {'message': 'File extension not allowed'}, 400
        image = Images(
            image_url=file.filename
        )
        db.session.add(image)
        db.session.commit()
        file.save(config.UPLOAD_FOLDER + file.filename)
        return {'message': 'Image uploaded successfully'}, 200

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
    
    def get(self):
        image = db.session.execute(
            """
            SELECT id, name, CONCAT('/', image_url) as image
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