from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ecommerce.api.schemas import UserSchema, ChangeShippingSchema, GetBalanceSchema
from ecommerce.models import User, Orders, Order_Products, Products, Product_Images, Images
from ecommerce.extensions import db
from ecommerce.commons.pagination import paginate


class UserResource(Resource):
    """Creation and get_detail
    ---
    get:
      tags:
        - USERS
      summary: Get user detail
      description: Get user detail
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items: UserSchema
    """

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()

        if not user:
            return {'message': 'User not found'}, 404
        
        return jsonify(
            {
                'data': UserSchema().dump(user)
            }
        )
        
class ChangeShippingAddress(Resource):
    """Creation and get_detail
    ---
    post:
      tags:
        - USERS
      summary: Change shipping address
      description: Change shipping address
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: John Doe
                phone_number:
                  type: string
                  example: 08123456789
                address:
                  type: string
                  example: Jl. Raya Kebon Jeruk No. 1
                city:
                  type: string
                  example: Jakarta Barat
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items: ChangeShippingSchema
    """
  
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return {'message': 'User not found'}, 404
        data = request.get_json()
        user.name = data['name']
        user.phone_number = data['phone_number']
        user.address = data['address']
        user.city = data['city']
        db.session.commit()
        return jsonify(
            {
                'message': 'success',
                'data': ChangeShippingSchema().dump(user)
            }
        )

class Balance(Resource):
    """Creation and get_detail
    ---
    post:
      tags:
        - USERS
      summary: Top up balance
      description: Top up balance
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                balance:
                  type: integer
                  example: 100000
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items: UserSchema
    """
  
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        balance = request.json['amount']
        user = User.query.filter_by(id=user_id).first()
        user.balance = user.balance + balance
        db.session.commit()
        
        # Enable Access-Control-Allow-Origin
        response = jsonify(
            {
                'message': 'Top Up Success',
                'description': 'Your Top Up Has Been Added To Your Balance'
            }        
        )
        
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

      

class GetBalance(Resource):
    """Creation and get_detail

    ---
    get:
      tags:
        - USERS
      summary: Get balance
      description: Get balance
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items: GetBalanceSchema
    """

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()
      
        if not user:
            return {'message': 'User not found'}, 404
        
        return jsonify(
            {
                'data': GetBalanceSchema().dump(user)
            }
        )
      
class GetUserOrderDetails(Resource):
    """Creation and get_detail
    ---
    get:
      tags:
        - USERS
      summary: Get user order details
      description: Get user order details
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items: UserSchema
    """

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = db.session.execute(
            """
            SELECT u.name, u.phone_number, u.address, u.city, orders.id, orders.shipping_method, orders.created_at, orders.shipping_price, orders.shipping_method, order__products.quantity, order__products.size, products.title, products.price, images.image_url, products.id, products.status
            FROM "user" u
            JOIN orders ON u.id = orders.user_id
            JOIN order__products ON orders.id = order__products.order_id
            JOIN products ON order__products.product_id = products.id
            JOIN product__images ON products.id = product__images.product_id
            JOIN images ON product__images.image_id = images.id
            WHERE orders.user_id = :user_id
            """,
            {'user_id': user_id}
        ).fetchall()
        
        if not user:
           return {'data': []}
          
        return jsonify(
            {
              "data" :[
                {
                'id': user[0][4],
                'created_at': user[0][6],
                'products' : [
                    {
                        'id': user[0][14],
                        'details': {
                            'quantity': user[0][9],
                            'size': user[0][10],
                        },
                        'price': user[0][12],
                        'image': user[0][13],
                        'name': user[0][11],
                    }
                ],
                # 'status': user[0][15],
                'shipping_method': user[0][8],
                'shipping_address': {
                    'name': user[0][0],
                    'phone_number': user[0][1],
                    'address': user[0][2],
                    'city': user[0][3],
                }
            }
        ]
        }
        )
      
                
        