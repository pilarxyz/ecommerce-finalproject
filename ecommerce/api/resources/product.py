from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ecommerce.api.schemas import ProductSchema
from ecommerce.models import Products, Product_Images, Images
from ecommerce.extensions import db, ma

from ecommerce.commons.pagination import paginate

class ProductList(Resource):
    """Creation and get_all
  
    ---
    get:
      tags:
        - PRODUCTS
      summary: Get all products
      description: Get all products
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  products:
                    type: array
                    items: ProductSchema
    """
    
    def get(self):
        products = db.session.execute(
            """
            SELECT products.id, products.title, products.product_detail, products.price, products.condition, products.category_id, images.image_url AS image
            FROM products
            JOIN product__images ON products.id = product__images.product_id
            JOIN images ON product__images.image_id = images.id
            """
        ).fetchall()
        return jsonify(
            {
                "data": ProductSchema(many=True).dump(products),
                "total_rows": len(products)
            }
        )
                      
      
        if not products:
          return {'message': 'Products not found'}, 404
    
    def error_handler(self, error):
        return {'message': str(error)}, 400