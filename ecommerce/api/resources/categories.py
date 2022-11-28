from flask import request
from flask_restful import Resource

from ecommerce.api.schemas import CategoryImageSchema
from ecommerce.models import Categories, Images, Products, Product_Images
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
                  data:
                    type: array
                    items: CategoryImageSchema
    """

    def get(self):
        
        category = db.session.execute(
                """
                SELECT categories.id, categories.created_at, categories.title, images.image_url AS image FROM categories
                LEFT JOIN products ON categories.id = products.category_id AND products.id = (SELECT id FROM products WHERE category_id = categories.id LIMIT 1)
                LEFT JOIN product__images ON products.id = product__images.product_id AND product__images.id = (SELECT id FROM product__images WHERE product_id = products.id LIMIT 1)
                LEFT JOIN images ON product__images.image_id = images.id
                """
            ).fetchall()
        if not category:
            return {'message': 'Category not found'}, 404
          
        return {'data': CategoryImageSchema(many=True).dump(category)}, 200
        

    def error_handler(self, error):
        return {'message': str(error)}, 400