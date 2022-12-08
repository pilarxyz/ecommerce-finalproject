from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ecommerce.api.schemas import ProductSchema, ProductDetailSchema
from ecommerce.models import Orders, Order_Products, Products, Product_Images, Images, User, Carts
from ecommerce.extensions import db, ma

class CreateOrder(Resource):
    """Create order
    ---
    post:
        tags:
            - ORDERS
        summary: Create order
        description: Create order
        requestBody:
            content:
                application/json:
                    schema:
                        type: object
    """
    
# Catatan:
# - Hanya bisa diakses oleh user yang sudah login
# - Akan mengurangi balance user berdasarkan total harga
# - Jika balance kurang dari total harga, return error
# - Akan menghapus semua cart yang ada di user tersebut
# method post
# shipping_method “Same day”
# shipping_address {
#  "name": "address name",
#  "phone_number": "082713626",
#  "address" : "22, ciracas, east jakarta",
#  "city": "Jakarta
# }

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()
        
        # get cart from user
        carts = db.session.query(Carts).filter_by(user_id=user_id).all()
        
        # get total price
        total_price = 0
        for cart in carts:
            total_price += cart.product.price * cart.quantity
        
        # check balance
        if user.balance < total_price:
            return jsonify({
                "message": "Balance is not enough"
            })
        
#         shipping_address: 
# address: "Jl. Raya Kebon Jeruk No. 1"
# city: "Jakarta Barat"
# name: "John Doe"
# phone_number: "08123456789"
# payload
        # create order
        order = Orders(
            user_id=user_id,
            shipping_method=request.json['shipping_method'],
            address=request.json['shipping_address']['address'],
            address_name=request.json['shipping_address']['name'],
            city=request.json['shipping_address']['city'],
            phone_number=request.json['shipping_address']['phone_number'],
            shipping_price=total_price,
            status="pending"
        )
        db.session.add(order)
        db.session.commit()
        
        # create order_product
        for cart in carts:
            order_product = Order_Products(
                order_id=order.id,
                product_id=cart.product_id,
                quantity=cart.quantity,
                size=cart.size,
            )
            db.session.add(order_product)
            db.session.commit()
        
        # delete cart
        for cart in carts:
            db.session.delete(cart)
            db.session.commit()
        
        # update balance
        user.balance -= total_price
        db.session.commit()
        
        return jsonify({
            "message": "Order success"
        })