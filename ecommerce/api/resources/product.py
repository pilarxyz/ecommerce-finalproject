from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ecommerce.api.schemas import ProductSchema, ProductDetailSchema
from ecommerce.models import Products, Product_Images, Images, Categories, User
from ecommerce.extensions import db, ma
from ecommerce import config
import base64

from ecommerce.commons.pagination import paginate

class ProductList(Resource):
# page 1
# page_size 100
# sort_by Price a_z, Price z_a
# category Id category a, id category b
# price 0,10000
# condition used
# product_name name

    """Creation and get_detail
    
    ---
    get:
      tags:
        - PRODUCTS
      summary: Get product list
      description: Get product list
      parameters:
        - in: query
          name: page
          schema:
            type: integer
        - in: query
          name: page_size
          schema:
            type: integer
        - in: query
          name: sort_by
          schema:
            type: string
        - in: query
          name: category
          schema:
            type: string
        - in: query
          name: price
          schema:
            type: string
        - in: query 
          name: condition
          schema:
            type: string
        - in: query 
          name: product_name
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
                    items: ProductSchema
    """
  
    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 100, type=int)
        sort_by = request.args.get('sort_by', 'Price a_z', type=str)
        category = request.args.get('category', '', type=str)
        price = request.args.get('price', '', type=str)
        condition = request.args.get('condition', '', type=str)
        product_name = request.args.get('product_name', '', type=str)
        
        products = db.session.execute(
            """
            SELECT products.id, products.title, products.product_detail as description, products.price, products.condition, products.category_id, images.image_url AS image
            FROM products
            JOIN Categories ON products.category_id = categories.id
            JOIN product__images ON products.id = product__images.product_id
            JOIN images ON product__images.image_id = images.id
            """
        ).fetchall()
        
        if category:
            products = [product for product in products if product.category_id == category]
          
        if price:
            price = price.split(',')
            products = [product for product in products if product.price >= price[0] and product.price <= price[1]]
            
        if condition:
            products = [product for product in products if product.condition == condition]
            
        if product_name:
            products = [product for product in products if product.title == product_name]
            
        if sort_by == 'Price a_z':
            products = sorted(products, key=lambda x: x.price)
            
        if sort_by == 'Price z_a':
            products = sorted(products, key=lambda x: x.price, reverse=True)
            
        if not products:
            return {'message': 'Products not found'}, 404
          
        return jsonify(
            {
                "data": ProductSchema(many=True).dump(products),
                "total_rows": len(products),
            }
        )
      


      
      
    #     products = db.session.execute(
    #         """
    #         SELECT products.id, products.title, products.product_detail as description, products.price, products.condition, products.category_id, images.image_url AS image
    #         FROM products
    #         JOIN Categories ON products.category_id = categories.id
    #         JOIN product__images ON products.id = product__images.product_id
    #         JOIN images ON product__images.image_id = images.id
    #         """
    #     ).fetchall()        
      
    #     if not products:
    #       return {'message': 'Products not found'}, 404
        
    #     return jsonify(
    #         {
    #             "data": ProductSchema(many=True).dump(products),
    #             "total_rows": len(products),
    #             "pagination": paginate(products)
    #         }
    #     )
    
    # def error_handler(self, error):
    #     return {'message': str(error)}, 400
      
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
            SELECT products.id, products.title, products.size, products.product_detail, products.price, products.condition, products.category_id, images.image_url as images_url, categories.title as category_name, array_agg(images.image_url) as images_url, array_agg(products.size) as size
            FROM products
            JOIN categories ON products.category_id = categories.id
            JOIN product__images ON products.id = product__images.product_id
            JOIN images ON product__images.image_id = images.id
            WHERE products.id = :id
            GROUP BY products.id, products.title, products.product_detail, products.price, products.condition, products.category_id, images.image_url, categories.title
            """,
            {"id": id}
        ).fetchone()
      
        if not product:
          return {'message': 'Product not found'}, 404
        
        return jsonify(
            {
                "data": ProductDetailSchema().dump(product)
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
    
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        if not user.is_admin:
            return {'message': 'You are not admin'}, 403
        
        data = request.get_json()
        product = Products(
            title=data['product_name'],
            product_detail=data['description'],
            price=data['price'],
            condition=data['condition'],
            category_id=data['category'],
            size=data['size']
        )
        
        db.session.add(product)
        db.session.commit()
        

        image = data['images'][0]
        image = image.split(',')[1]
        image = base64.b64decode(image)
        image_name = f"{product.id}.png"
        with open(config.UPLOAD_FOLDER + '/' + image_name, 'wb') as f:
            f.write(image)
          
        
        # add image to database
        image = Images(
            name=data['product_name'],
            image_url=f"/static/images/{image_name}"
        )
        db.session.add(image)
        db.session.commit()
        
        # add product to product__images
        product_image = Product_Images(product_id=product.id, image_id=image.id)
        db.session.add(product_image)
        
        db.session.commit()
      
        return {'message': 'Product created successfully'}, 200
        
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
      
    @jwt_required()
    def put(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        if not user.is_admin:
            return {'message': 'You are not admin'}, 403
        
        data = request.get_json()
        product = Products.query.filter_by(id=id).first()
        if not product:
            return {'message': 'Product not found'}, 404
        
        product.title = data['product_name']
        product.product_detail = data['description']
        product.price = data['price']
        product.condition = data['condition']
        product.category_id = data['category']
        
        db.session.commit()
        
        image = data['images'][0]
        image = image.split(',')[1]
        image = base64.b64decode(image)
        image_name = f"{product.id}.png"
        with open(config.UPLOAD_FOLDER + '/' + image_name, 'wb') as f:
            f.write(image)
        
        # update image to database
        image = Images.query.filter_by(id=product.id).first()
        image.name = data['product_name']
        
        db.session.commit()
        
        return {'message': 'Product updated successfully'}, 200
        
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
    
    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        if not user.is_admin:
            return {'message': 'You are not admin'}, 403
        
        product_image = Product_Images.query.filter_by(product_id=id).first()
        if not product_image:
            return {'message': 'Product not found'}, 404
          
        db.session.delete(product_image)
        
        product = Products.query.filter_by(id=id).first()
        db.session.delete(product)
        
        db.session.commit()
        
        return {'message': 'Product deleted'}, 200 
      
    def error_handler(self, error):
        return {'message': str(error)}, 400
   