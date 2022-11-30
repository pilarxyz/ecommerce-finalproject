from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from flask_cors import CORS
from marshmallow import ValidationError
from ecommerce.extensions import apispec
from ecommerce.api.resources import UserResource, ProductList, BannerList, CategoryImageList, CategoriesList, ProductDetail, CartList, ShippingAdress
from ecommerce.api.schemas import UserSchema, ProductSchema, BannerSchema, CategoryImageSchema, CategoriesSchema, ProductDetailSchema, CartSchema, ShippingSchema



blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)
CORS(blueprint)

# add CORS support
# from flask_cors import CORS
# CORS(blueprint, resources={r"/api/*": {"origins": "*"}})


api.add_resource(ProductList, "/products", endpoint="products")
api.add_resource(ProductDetail, "/products/<string:id>", endpoint="product_by_id")
api.add_resource(BannerList, "/home/banner", endpoint="banners")
api.add_resource(CategoryImageList, "/home/category", endpoint="categoriesimages")
api.add_resource(CategoriesList, "/categories", endpoint="categories")
api.add_resource(CartList, "/cart", endpoint="carts")
api.add_resource(ShippingAdress, "/shipping_address", endpoint="shipping_addresses")
api.add_resource(UserResource, "/user", endpoint="user")




@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.components.schema("ProductSchema", schema=ProductSchema)
    apispec.spec.path(view=ProductList, app=current_app)
    apispec.spec.components.schema("BannerSchema", schema=BannerSchema)
    apispec.spec.path(view=BannerList, app=current_app)
    apispec.spec.components.schema("CategoryImageSchema", schema=CategoryImageSchema)
    apispec.spec.path(view=CategoryImageList, app=current_app)
    apispec.spec.components.schema("CategoriesSchema", schema=CategoriesSchema)
    apispec.spec.path(view=CategoriesList, app=current_app)
    apispec.spec.components.schema("ProductDetailSchema", schema=ProductDetailSchema)
    apispec.spec.path(view=ProductDetail, app=current_app)
    apispec.spec.components.schema("CartSchema", schema=CartSchema)
    apispec.spec.path(view=CartList, app=current_app)
    apispec.spec.components.schema("ShippingSchema", schema=ShippingSchema)
    apispec.spec.path(view=ShippingAdress, app=current_app)

@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
