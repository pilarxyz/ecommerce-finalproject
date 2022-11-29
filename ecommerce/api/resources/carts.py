from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ecommerce.api.schemas import CartSchema
from ecommerce.models import Carts
from ecommerce.extensions import db, ma, jwt

class CartList(Resource):
    """Creation and get_all

    ---
    get:
        tags:
            - CART
        summary: Get all carts
        description: Get all carts
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                carts:
                                    type: array
                                    items: CartSchema
    """
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        carts = db.session.execute(
            """
            SELECT carts.id, carts.user_id, carts.product_id, carts.quantity, products.title, products.price
            FROM carts
            INNER JOIN products ON carts.product_id = products.id
            WHERE carts.user_id = :user_id
            """,
            {"user_id": user_id}
        ).fetchall()
        
        if not carts:
            return {'message': 'Cart not found'}, 404
        
        return {'data': CartSchema(many=True).dump(carts)}, 200
    


    # @jwt_required()
    # def post(self):
    #     user_id = get_jwt_identity()
    #     data = request.get_json()
    #     cart = Carts(user_id=user_id, product_id=data['product_id'], quantity=data['quantity'])
    #     db.session.add(cart)
    #     db.session.commit()
    #     return {'message': 'Cart added'}, 200