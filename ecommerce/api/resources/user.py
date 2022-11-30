from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ecommerce.api.schemas import UserSchema, ChangeShippingSchema
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
        user = db.session.execute(
            """
            UPDATE users
            SET shipping_address = :shipping_address
            WHERE id = :user_id
            """,
            {"shipping_address": request.json['shipping_address'], "user_id": user_id}
        )
        db.session.commit()
        return {'message': 'Shipping address changed'}, 200
        
        return jsonify(
            {
                'data': UserSchema().dump(user)
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
        user = db.session.execute(
            """
            UPDATE users
            SET balance = balance + :balance
            WHERE id = :user_id
            """,
            {"balance": request.json['balance'], "user_id": user_id}
        )
        db.session.commit()
        return {'message': 'Balance topped up'}, 200
      
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = db.session.execute(
            """
            SELECT balance
            FROM users
            WHERE id = :user_id
            """,
            {"user_id": user_id}
        ).fetchone()
        return {'balance': user[0]}, 200