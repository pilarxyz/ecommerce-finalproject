from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ecommerce.api.schemas import ProductSchema, ProductDetailSchema
from ecommerce.models import Products, Product_Images, Images, Categories, User
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
            SELECT products.id, products.title, products.product_detail as description, products.price, products.condition, products.category_id, images.image_url AS image
            FROM products
            JOIN Categories ON products.category_id = categories.id
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
            SELECT products.id, products.title, products.product_detail, products.size, products.price, products.condition, products.category_id, images.image_url as images_url, categories.title as category_name
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
      
      
# only admin can create product
class ProductCreate(Resource):
    """Creation and get_detail
    
    ---
    post:
      tags:
        - PRODUCTS
      summary: Create product
      description: Create product
      parameters:
        - in: body
          name: body
          schema:
            type: object
            properties:
              title:
                type: string
              product_detail:
                type: string
              size:
                type: string
              price:
                type: integer
              condition:
                type: string
              category_id:
                type: integer
              image_url:
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
    
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        if not user.is_admin:
            return {'message': 'You are not admin'}, 403
        
        data = request.get_json()
        product = Products(
            title=data['title'],
            product_detail=data['product_detail'],
            size=data['size'],
            price=data['price'],
            condition=data['condition'],
            category=data['category_id']
        )
        
        db.session.add(product)
        db.session.commit()
        
        image = Images(
            image_url=data['image_url']
        )
        
        db.session.add(image)
        db.session.commit()
        
        product_image = Product_Images(
            product_id=product.id,
            image_id=image.id
        )
        
        db.session.add(product_image)
        db.session.commit()
        
        return {'message': 'Product added'}, 200
    
    def error_handler(self, error):
        return {'message': str(error)}, 400
      

# only admin can update product
class ProductUpdate(Resource):
    """Creation and get_detail
    
    ---
    put:
      tags:
        - PRODUCTS
      summary: Update product
      description: Update product
      parameters:
        - in: path
          name: id
          schema:
            type: string
        - in: body
          name: body
          schema:
            type: object
            properties:
              title:
                type: string
              product_detail:
                type: string
              size:
                type: string
              price:
                type: integer
              condition:
                type: string
              category_id:
                type: integer
              image_url:
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
    
    @jwt_required
    def put(self, id):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        if not user.is_admin:
            return {'message': 'You are not admin'}, 403
        
        data = request.get_json()
        product = Products.query.filter_by(id=id).first()
        if not product:
            return {'message': 'Product not found'}, 404
        
        product.title = data['title']
        product.product_detail = data['product_detail']
        product.size = data['size']
        product.price = data['price']
        product.condition = data['condition']
        product.category_id = data['category_id']
        
        db.session.commit()
        
        image = Images.query.filter_by(id=product.id).first()
        if not image:
            return {'message': 'Image not found'}, 404
        
        image.image_url = data['image_url']
        
        db.session.commit()
        
        return {'message': 'Product updated'}, 200
    
    def error_handler(self, error):
        return {'message': str(error)}, 400
      
  
# only admin can delete product
class ProductDelete(Resource):
    """Creation and get_detail
    
    ---
    delete:
      tags:
        - PRODUCTS
      summary: Delete product
      description: Delete product
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
    
    @jwt_required
    def delete(self, id):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        if not user.is_admin:
            return {'message': 'You are not admin'}, 403
        
        product = Products.query.filter_by(id=id).first()
        if not product:
            return {'message': 'Product not found'}, 404
        
        db.session.delete(product)
        db.session.commit()
        
        return {'message': 'Product deleted'}, 200
    
    def error_handler(self, error):
        return {'message': str(error)}, 400
      
# class ProductCreate(Resource):
#     """Creation and get_all
  
#     ---
#     post:
#       tags:
#         - PRODUCTS
#       summary: Create new product
#       description: Create new product
#       requestBody:
#         content:
#           application/json:
#             schema:
#               type: object
#               properties:
#                 title:
#                   type: string
#                 product_detail:
#                   type: string
#                 size:
#                   type: string
#                 price:
#                   type: integer
#                 condition:
#                   type: string
#                 category_id:
#                   type: integer
#                 image_url:
#                   type: string
#       responses:
#         200:
#           content:
#             application/json:
#               schema:
#                 type: object
#                 properties:
#                   product:
#                     type: array
#                     items: ProductSchema
#     """
#     @jwt_required()
#     def post(self):
#         data = request.get_json()
        
#         product = Products(
#             title=data['title'],
#             product_detail=data['product_detail'],
#             size=data['size'],
#             price=data['price'],
#             condition=data['condition'],
#             category_id=data['category_id']
#         )
        
#         db.session.add(product)
#         db.session.commit()
        
#         image = Images(
#             image_url=data['image_url']
#         )
        
#         db.session.add(image)
#         db.session.commit()
        
#         product_image = Product_Images(
#             product_id=product.id,
#             image_id=image.id
#         )
        
#         db.session.add(product_image)
#         db.session.commit()
        
#         return {'message': 'Product added'}, 201
    
#     def error_handler(self, error):
#         return {'message': str(error)}, 400
      
# class ProductUpdate(Resource):
#     """Creation and get_all
  
#     ---
#     put:
#       tags:
#         - PRODUCTS
#       summary: Update product
#       description: Update product
#       parameters:
#         - in: path
#           name: id
#           schema:
#             type: string
#       requestBody:
#         content:
#           application/json:
#             schema:
#               type: object
#               properties:
#                 title:
#                   type: string
#                 product_detail:
#                   type: string
#                 size:
#                   type: string
#                 price:
#                   type: integer
#                 condition:
#                   type: string
#                 category_id:
#                   type: integer
#                 image_url:
#                   type: string
#       responses:
#         200:
#           content:
#             application/json:
#               schema:
#                 type: object
#                 properties:
#                   product:
#                     type: array
#                     items: ProductSchema
#     """
    
#     @jwt_required()    
#     def put(self, id):
#         data = request.get_json()
        
#         product = Products.query.filter_by(id=id).first()
  
#         if not product:
#           return {'message': 'Product not found'}, 404
      
#         product.title = data['title']
#         product.product_detail = data['product_detail']
#         product.size = data['size']
#         product.price = data['price']
#         product.condition = data['condition']
#         product.category_id = data['category_id']
      
#         db.session.commit()
      
#         image = Images.query.filter_by(id=product.id).first()
      
#         if not image:
#           return {'message': 'Image not found'}, 404
      
#         image.image_url = data['image_url']
      
#         db.session.commit()
      
#         return {'message': 'Product updated'}, 200
      
#     def error_handler(self, error):
#         return {'message': str(error)}, 400
      
# class ProductDelete(Resource):
#     """Creation and get_all
  
#     ---
#     delete:
#       tags:
#         - PRODUCTS
#       summary: Delete product
#       description: Delete product
#       parameters:
#         - in: path
#           name: id
#           schema:
#             type: string
#       responses:
#         200:
#           content:
#             application/json:
#               schema:
#                 type: object
#                 properties:
#                   product:
#                     type: array
#                     items: ProductSchema
#     """
    
#     @jwt_required()    
#     def delete(self, id):
#         product = Products.query.get(id)
        
#         if not product:
#           return {'message': 'Product not found'}, 404
        
#         db.session.delete(product)
#         db.session.commit()
        
#         return {'message': 'Product deleted'}, 201
    
#     def error_handler(self, error):
#         return {'message': str(error)}, 400