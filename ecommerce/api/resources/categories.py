from flask import request
from flask_restful import Resource

from ecommerce.api.schemas import CategoryImageSchema
from ecommerce.models import Categories
from ecommerce.models import Images
from ecommerce.extensions import db, ma

class CategoryImageList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - home
      summary: Get all categories
      description: Get all categories
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  categories:
                    type: array
                    items: CategorySchema
    """

    def get(self):
        # create query category get images
        category = Categories.query.filter_by(id=category_id).first()
        images = Images.query.filter_by(category_id=category_id).all()
        return {'data': CategoryImageSchema(many=True).dump(images)}, 200
        

    def error_handler(self, error):
        return {'message': str(error)}, 400