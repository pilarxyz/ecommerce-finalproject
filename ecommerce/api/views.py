from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from flask_cors import CORS, cross_origin
from marshmallow import ValidationError
from ecommerce.extensions import apispec
from ecommerce.api.resources import UserResource, ProductList, BannerList, CategoryImageList, CategoriesList, ProductDetail, CartList, ShippingAdress, Balance, ChangeShippingAddress, GetBalance, GetOrdersUser, TotalSales, ProductCreate, ProductUpdate, ProductDelete, CategoriesDetail, CategoriesCreate, CategoriesUpdate, CategoriesDelete, ShippingPrice, Cart, DeleteCart, GetImage, UploadImage, GetUserOrderDetails, CreateOrder, SearchWithImages
from ecommerce.api.schemas import UserSchema, ProductSchema, BannerSchema, CategoryImageSchema, CategoriesSchema, ProductDetailSchema, CartSchema, ShippingSchema, ChangeShippingSchema, GetBalanceSchema, ListOrdersSchema, ShippingAdressSchema


blueprint = Blueprint("api", __name__, url_prefix="")
api = Api(blueprint)

#add cross origin to all routes
CORS(blueprint)

#product
api.add_resource(ProductList, "/products", endpoint="products")
api.add_resource(ProductDetail, "/products/<string:id>", endpoint="product_by_id")
api.add_resource(ProductCreate, "/products", endpoint="product_create")
api.add_resource(ProductUpdate, "/products", endpoint="product_update")
api.add_resource(ProductDelete, "/products/<string:id>", endpoint="product_delete")
api.add_resource(SearchWithImages, "/products/search_image", endpoint="search")

#home
api.add_resource(BannerList, "/home/banner", endpoint="banners")
api.add_resource(CategoryImageList, "/home/category", endpoint="categoriesimages")
api.add_resource(GetImage, "/image", endpoint="get_image")
api.add_resource(UploadImage, "/image", endpoint="upload_image")


#order
api.add_resource(CreateOrder, "/order", endpoint="create_order")

#categories
api.add_resource(CategoriesList, "/categories", endpoint="categories")
api.add_resource(CategoriesDetail, "/categories/<string:id>", endpoint="category_by_id")
api.add_resource(CategoriesCreate, "/categories", endpoint="category_create")
api.add_resource(CategoriesUpdate, "/categories/<string:id>", endpoint="category_update")
api.add_resource(CategoriesDelete, "/categories/<string:id>", endpoint="category_delete")

#cart
api.add_resource(CartList, "/cart", endpoint="carts")
api.add_resource(ShippingAdress, "/user/shipping_address", endpoint="shipping_addresses")
api.add_resource(ShippingPrice, "/shipping_price", endpoint="shipping_price")
api.add_resource(Cart, "/cart", endpoint="cart")
api.add_resource(DeleteCart, "/cart/<string:id>", endpoint="delete_cart")

#user
api.add_resource(UserResource, "/user", endpoint="user")
api.add_resource(ChangeShippingAddress, "/user/shipping_address", endpoint="change_shipping_address")
api.add_resource(Balance, "/user/balance", endpoint="balance")
api.add_resource(GetUserOrderDetails, "/user/order", endpoint="user_order_details")
api.add_resource(GetBalance, "/user/balance", endpoint="get_balance")
api.add_resource(GetOrdersUser, "/orders", endpoint="get_orders_user")
api.add_resource(TotalSales, "/sales", endpoint="total_sales")




@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    
    #product
    apispec.spec.components.schema("ProductSchema", schema=ProductSchema)
    apispec.spec.path(view=ProductList, app=current_app)
    apispec.spec.components.schema("ProductDetailSchema", schema=ProductDetailSchema)
    apispec.spec.path(view=ProductDetail, app=current_app)
    apispec.spec.path(view=ProductCreate, app=current_app)
    apispec.spec.path(view=ProductUpdate, app=current_app)
    apispec.spec.path(view=ProductDelete, app=current_app)
    apispec.spec.path(view=SearchWithImages, app=current_app)


    apispec.spec.components.schema("BannerSchema", schema=BannerSchema)
    apispec.spec.path(view=BannerList, app=current_app)
    apispec.spec.path(view=GetImage, app=current_app)
    apispec.spec.path(view=UploadImage, app=current_app)
    
    #categories
    apispec.spec.components.schema("CategoryImageSchema", schema=CategoryImageSchema)
    apispec.spec.path(view=CategoryImageList, app=current_app)
    apispec.spec.components.schema("CategoriesSchema", schema=CategoriesSchema)
    apispec.spec.path(view=CategoriesList, app=current_app)
    apispec.spec.path(view=CategoriesDetail, app=current_app)
    apispec.spec.path(view=CategoriesCreate, app=current_app)
    apispec.spec.path(view=CategoriesUpdate, app=current_app)
    apispec.spec.path(view=CategoriesDelete, app=current_app)

    # cart
    apispec.spec.components.schema("CartSchema", schema=CartSchema)
    apispec.spec.path(view=CartList, app=current_app)
    apispec.spec.components.schema("ShippingSchema", schema=ShippingSchema)
    apispec.spec.path(view=ShippingAdress, app=current_app)
    apispec.spec.path(view=ShippingPrice, app=current_app)
    apispec.spec.path(view=Cart, app=current_app)
    apispec.spec.path(view=DeleteCart, app=current_app)
    
    
    apispec.spec.components.schema("ChangeShippingSchema", schema=ShippingSchema)
    apispec.spec.path(view=ChangeShippingAddress, app=current_app)
    apispec.spec.components.schema("GetBalanceSchema", schema=GetBalanceSchema)
    apispec.spec.path(view=GetBalance, app=current_app)
    apispec.spec.path(view=Balance, app=current_app)
    apispec.spec.components.schema("ListOrdersSchema", schema=ListOrdersSchema)
    apispec.spec.path(view=GetOrdersUser, app=current_app)
    apispec.spec.path(view=TotalSales, app=current_app)
    apispec.spec.path(view=GetUserOrderDetails, app=current_app)
    
    #order
    apispec.spec.path(view=CreateOrder, app=current_app)
    

@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
