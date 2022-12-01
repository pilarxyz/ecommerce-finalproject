from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ecommerce.api.schemas import CartSchema, ShippingSchema, ShippingAdressSchema
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
    
class Cart(Resource):
#   API untuk menambahkan produk menuju menu ‘cart’ pada user
# Bobot nilai: 2 poin
# Catatan:
# - Hanya bisa di panggil oleh user yang sudah login, jika belum login,
# return error message
# - Items di cart bersifat unique berdasarkan item_id dan size
# - Jika menambahkan item yang mempunyai id dan size yang sama ke
# dalam cart, akan menambahkan quantity item di cart tersebut

    """Creation and get_all

    ---
    post:
        tags:
            - CART
        summary: Add product to cart
        description: Add product to cart
        requestBody:
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            product_id:
                                type: string
                            size:
                                type: string
                            quantity:
                                type: integer
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
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        product_id = data['product_id']
        size = data['size']
        quantity = data['quantity']
        cart = Carts.query.filter_by(user_id=user_id, product_id=product_id, size=size).first()
        if cart:
            cart.quantity += quantity
            db.session.commit()
            return {'message': 'Cart updated'}, 200
        else:
            cart = Carts(user_id=user_id, product_id=product_id, size=size, quantity=quantity)
            db.session.add(cart)
            db.session.commit()
            return {'message': 'Item added to cart'}, 200      

class ShippingPrice(Resource):
    """Get shipping price

    ---
    get:
        tags:
            - CART
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
                                    items: ShippingSchema
    """
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        carts = db.session.execute(
            """
            SELECT SUM(products.price * carts.quantity) as total
            FROM carts
            JOIN products ON carts.product_id = products.id
            WHERE carts.user_id = :user_id
            """,
            {"user_id": user_id}
        ).fetchall()
        
        if not carts:
            return {'message': 'Cart not found'}, 404
        
# Akan ada 2 jenis shipping method:
# - Regular:
# - Jika total harga item < 200: Shipping price merupakan 15% dari
# total harga item yang dibeli
# - Jika total harga item >= 200: Shipping price merupakan 20%
# dari total harga item yang dibeli
# - Next Day:
# - Jika total harga item < 300: Shipping price merupakan 20% dari
# total harga item yang dibeli
# - Jika total harga item >= 300: Shipping price merupakan 25%
# dari total harga item yang dibeli
        
        shipping = []
        for cart in carts:
            if cart.total < 200:
                shipping.append({
                    'name': 'Regular',
                    'price': cart.total * 0.15
                })
            else:
                shipping.append({
                    'name': 'Regular',
                    'price': cart.total * 0.2
                })
            if cart.total < 300:
                shipping.append({
                    'name': 'Next Day',
                    'price': cart.total * 0.2
                })
            else:
                shipping.append({
                    'name': 'Next Day',
                    'price': cart.total * 0.25
                })
                
        return jsonify(
            {
                'data': ShippingSchema(many=True).dump(shipping)
            }
        )
        
        
class ShippingAdress(Resource):
    """Get shipping address

    ---
    get:
        tags:
            - CART
        summary: Get shipping address
        description: Get shipping address
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                shipping:
                                    type: array
                                    items: ShippingAdressSchema
    """
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'User not found'}, 404
        return jsonify(
            {
                'data': ShippingAdressSchema().dump(user)
            }
        )

class DeleteCart(Resource):
    """Delete cart

    ---
    delete:
        tags:
            - CART
        summary: Delete cart
        description: Delete cart
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                message:
                                    type: string
    """
    
    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        cart = Carts.query.filter_by(user_id=user_id).first()
        if not cart:
            return {'message': 'Cart not found'}, 404
        db.session.delete(cart)
        db.session.commit()
        return {'message': 'Cart deleted'}, 200