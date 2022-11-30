from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ecommerce.api.schemas import ProductSchema, ProductDetailSchema
from ecommerce.models import Products, Product_Images, Images, Categories
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
      
        if not products:
          return {'message': 'Products not found'}, 404
        
        return jsonify(
            {
                "data": ProductSchema(many=True).dump(products),
                "total_rows": len(products)
            }
        )
    
    def error_handler(self, error):
        return {'message': str(error)}, 400
      
class ProductDetail(Resource):
    """Creation and get_detail
    
    ---
    get:
      tags:
        - PRODUCTS
      summary: Get product detail
      description: Get product detail
      parameters:
        - in: path
          name: id
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  product:
                    type: array
                    items: ProductDetailSchema
    """
    
    
    def get(self, id):
        product = db.session.execute(
            """
            SELECT products.id, products.title, products.product_detail, products.size, products.price, products.condition, products.category_id, images.image_url as image_url, categories.title as category_name
            FROM products
            JOIN categories ON products.category_id = categories.id
            JOIN product__images ON products.id = product__images.product_id
            JOIN images ON product__images.image_id = images.id
            WHERE products.id = :id
            """,
            {"id": id}
        ).fetchone()
      
        if not product:
          return {'message': 'Product not found'}, 404
        
        return jsonify(
            {
                "data": ProductDetailSchema().dump(product),
            }
        )
      
    def error_handler(self, error):
        return {'message': str(error)}, 400