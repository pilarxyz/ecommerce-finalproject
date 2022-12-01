from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ecommerce.api.schemas import UserSchema, ChangeShippingSchema, GetBalanceSchema
from ecommerce.models import User
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
      parameters:
        - in: body
          name: body
          description: Change shipping address
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
        # user = db.session.execute(
        #     """
        #     UPDATE user
        #     SET shipping_address = 
        #     WHERE id = :user_id
        #     """,
        #     {'address': request.json['address'], 'name': request.json['name'], 'phone_number': request.json['phone_number'], 'city': request.json['city'], 'user_id': user_id }
        # )
        user_update = db.session.query(User).filter_by(id=user_id).first()
        user_update.shipping_address = request.json['address']
        user_update.shipping_name = request.json['name']
        user_update.shipping_phone_number = request.json['phone_number']
        user_update.shipping_city = request.json['city']
        db.session.commit()

        if not user:
            return {'message': 'User not found'}, 404
        
        return jsonify(
            {
                'message': 'Update Success'
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
        balance = request.json['balance']
        user = User.query.filter_by(id=user_id).first()
        user.balance = user.balance + balance
        db.session.commit()

        return jsonify(
            {
                'message': 'Top Up Success',
                'description': 'Your Top Up Has Been Added To Your Balance'
            }
        )
      

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
            SELECT 
            FROM user, orders, order__products
            WHERE user.id = orders.user_id
            """,
            {"user_id": user_id}
        ).fetchone()
        
        return jsonify(
            {
                'data': UserSchema().dump(user)
            }
        )
 
#   Berupa informasi mengenai pesanan yang telah dilakukan oleh pengguna.
# Bobot nilai: 1 poin
# Catatan: “price” dari products disini adalah harga asli dari product * jumlah
# product yang di checkout.
# Metode: GET


# class GetUserOrderHistory(Resource):
#     """Creation and get_detail
#     ---
#     get:
#       tags:
#         - USERS
#       summary: Get user order history
#       description: Get user order history
#       responses:
#         200:
#           content:
#             application/json:
#               schema:
#                 type: object
#                 properties:
#                   users:
#                     type: array
#                     items: UserSchema
#     """
  
