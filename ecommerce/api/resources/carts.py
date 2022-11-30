from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ecommerce.api.schemas import CartSchema, ShippingSchema
from ecommerce.models import Carts, Products, Product_Images, Images, User, Orders, Order_Products
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
            # """
            # SELECT carts.id, carts.user_id, carts.product_id, carts.quantity, products.title, products.price
            # FROM carts
            # INNER JOIN products ON carts.product_id = products.id
            # WHERE carts.user_id = :user_id
            # """,
            # price
            """
            SELECT carts.id, carts.user_id, carts.product_id, products.title as name, products.price, images.image_url as image, json_build_object('size', products.size, 'quantity', carts.quantity) as details
            FROM carts
            JOIN products ON carts.product_id = products.id
            JOIN product__images ON products.id = product__images.product_id
            JOIN images ON product__images.image_id = images.id
            WHERE carts.user_id = :user_id
            GROUP BY carts.id, carts.user_id, carts.product_id, products.title, products.price, images.image_url, products.size, carts.quantity
            """,
            {"user_id": user_id}
        ).fetchall()
        
        if not carts:
            return {'message': 'Cart not found'}, 404
        
        
        return jsonify(
            {
                'data': CartSchema(many=True).dump(carts) 
            }
        )
        
    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        cart = Carts.query.filter_by(user_id=user_id).first()
        if not cart:
            return {'message': 'Cart not found'}, 404
        db.session.delete(cart)
        db.session.commit()
        return {'message': 'Cart deleted'}, 200
    
class ShippingAdress(Resource):
    """Creation and get_all
    
    ---
    get:
        tags:
            - USERS
        summary: Get shipping adress
        description: Get shipping adress
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                shipping:
                                    type: array
                                    items: ShippingSchema
    """
    
    @jwt_required()
    # get shipping address
    def get(self):
        user_id = get_jwt_identity()
        shipping_address = db.session.execute(
            """
            SELECT 
            FROM user, orders, order__products
            WHERE user.id = orders.user_id
            """,
            {"user_id": user_id}
        ).fetchone()
        
        return schema.dump(shipping_address)
    
        if not shipping_address:
            return {'message': 'Shipping address not found'}, 404
        
        return jsonify(
            {
                'data': ShippingSchema(many=True).dump(shipping_address)
            }
        )  
        
# get shipping price
class ShippingPrice(Resource):
    """Creation and get_all
    
    ---
    get:
        tags:
            - SHIPPING
        summary: Get shipping price
        description: Get shipping price
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                shipping:
                                    type: array
                                    items: ShippingPriseSchema
    """
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        shipping_price = db.session.execute(
            """
            SELECT shipping_price
            FROM users
            WHERE id = :user_id
            """,
            {"user_id": user_id}
        ).fetchone()
        
        if not user_id:
            return {'message': 'Login first'}, 404
        
        if not carts:
            return {'message': 'Cart is empty'}, 404
        
        return jsonify(
            {
                'data': ShippingPriceSchema(many=True).dump(shipping_price)
            }
        )