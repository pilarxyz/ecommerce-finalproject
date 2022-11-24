from flask import request
from flask_restful import Resource
from ecommerce.api.schemas import ProductSchema
from ecommerce.models import Products
from ecommerce.extensions import db, ma

from ecommerce.commons.pagination import paginate

class ProductResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - products
      summary: Get a product
      description: Get a single product by ID
      parameters:
        - in: path
          name: product_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  product: ProductSchema
        404:
          description: product does not exists
    put:
      tags:
        - products
      summary: Update a product
      description: Update a single product by ID
      parameters:
        - in: path
          name: product_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              ProductSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: product updated
                  product: ProductSchema
        404:
          description: product does not exists
    delete:
      tags:
        - products
      summary: Delete a product
      description: Delete a single product by ID
      parameters:
        - in: path
          name: product_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: product deleted
        404:
          description: product does not exists
    """

    def get(self, product_id):
        schema = ProductSchema()
        product = Product.query.get_or_404(product_id)
        return {"product": schema.dump(product)}

    def put(self, product_id):
        schema = ProductSchema(partial=True)
        product = Product.query.get_or_404(product_id)
        product, errors = schema.load(request.json, instance=product)
        if errors:
            return errors, 422
        db.session.commit()
        return {"msg": "product updated", "product": schema.dump(product)}
    
    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {"msg": "product deleted"}

class ProductList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - products
      summary: Get all products
      description: Get all products
      parameters:
        - in: query
          name: page
          schema:
            type: integer
        - in: query
          name: per_page
          schema:
            type: integer
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
                  total:
                    type: integer
                  pages:
                    type: integer
                  page:
                    type: integer
    post:
      tags:
        - products
      summary: Create a product
      description: Create a product
      requestBody:
        content:
          application/json:
            schema:
              ProductSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: product created
                  product: ProductSchema
        422:
          description: invalid payload
    """

    def get(self):
        schema = ProductSchema(many=True)
        query = Products.query
        return paginate(query, schema)

    def post(self):
        schema = ProductSchema()
        product, errors = schema.load(request.json)
        if errors:
            return errors, 422
        db.session.add(product)
        db.session.commit()
        return {"msg": "product created", "product": schema.dump(product)}, 201