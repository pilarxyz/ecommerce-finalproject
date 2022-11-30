from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ecommerce.api.schemas import CategoriesSchema
from ecommerce.models import Categories
from ecommerce.extensions import db, ma

class CategoriesList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - CATEGORIES
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
                    items: CategoriesSchema
    """

    def get(self):
        categories = db.session.execute(
            """
            SELECT categories.id, categories.title
            FROM categories
            """
        ).fetchall()

        if not categories:
          return {'message': 'Categories not found'}, 404
        
        return {'data': CategoriesSchema(many=True).dump(categories)}, 200

    def error_handler(self, error):
        return {'message': str(error)}, 400

# access control allow origin

