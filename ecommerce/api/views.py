from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from ecommerce.extensions import apispec
from ecommerce.api.resources import UserResource, UserList, ProductList, BannerList, CategoryImageList, CategoriesList
from ecommerce.api.schemas import UserSchema, ProductSchema, BannerSchema, CategoryImageSchema, CategoriesSchema



blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")
api.add_resource(ProductList, "/products", endpoint="products")
api.add_resource(BannerList, "/home/banners", endpoint="banners")
api.add_resource(CategoryImageList, "/home/categories", endpoint="categoriesimages")
api.add_resource(CategoriesList, "/categories", endpoint="categories")



@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
    apispec.spec.components.schema("ProductSchema", schema=ProductSchema)
    apispec.spec.path(view=ProductList, app=current_app)
    apispec.spec.components.schema("BannerSchema", schema=BannerSchema)
    apispec.spec.path(view=BannerList, app=current_app)
    apispec.spec.components.schema("CategoryImageSchema", schema=CategoryImageSchema)
    apispec.spec.path(view=CategoryImageList, app=current_app)
    apispec.spec.components.schema("CategoriesSchema", schema=CategoriesSchema)
    apispec.spec.path(view=CategoriesList, app=current_app)

@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
