from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ecommerce.api.schemas import ListOrdersSchema
from ecommerce.models import User, Products, Categories, Orders, Order_Products, Product_Images, Images, Banners, Carts, Categories
from ecommerce.extensions import db, ma, jwt

# only admin can access this
class GetOrdersUser(Resource):
    """Get all orders from user

    ---
    get:
        tags:
            - ORDERS
        summary: Get all orders from user
        description: Get all orders from user
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                orders:
                                    type: array
                                    items: ListOrdersSchema
    """
    
    @jwt_required()
    def get(self):
        
        # if user is admin then get all orders from all users
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()
        if user.is_admin:
            # join orders with user, product,and order_products
            # orders = Orders.query.join(User, Orders.user_id == User.id).join(Order_Products, Orders.id == Order_Products.order_id).join(Products, Order_Products.product_id == Products.id).add_columns(Orders.id, Orders.user_id, Orders.created_at, User.name, Products.title, Products.price, Order_Products.quantity).all()
            orders = db.session.execute(
                """
                SELECT orders.id, orders.user_id, orders.created_at, "user".name as user_name, "user".email as user_email, SUM(products.price * order__products.quantity) as total
                FROM orders
                JOIN "user" ON orders.user_id = "user".id
                JOIN order__products ON orders.id = order__products.order_id
                JOIN products ON order__products.product_id = products.id
                GROUP BY orders.id, orders.user_id, orders.created_at, "user".name, "user".email
                """
            ).fetchall()
            
            return jsonify({
                "data": ListOrdersSchema(many=True).dump(orders)
            })
        
class TotalSales(Resource):
    """Get total sales

    ---
    get:
        tags:
            - HOME
        summary: Get total sales
        description: Get total sales
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                total_sales:
                                    type: integer
    """
    
    @jwt_required()
    def get(self):
        
        # if user is admin then get all orders from all users
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()
        if user.is_admin:
            total_sales = db.session.execute(
                """
                SELECT SUM(products.price * order__products.quantity) as total
                FROM orders
                JOIN order__products ON orders.id = order__products.order_id
                JOIN products ON order__products.product_id = products.id
                """
            ).fetchone()
            
            return jsonify({
                "data": {
                    "total": total_sales[0]
                }
            })
            

            
        
