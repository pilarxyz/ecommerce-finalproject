# create hello world api
from flask import Blueprint, current_app, jsonify
from flask_restful import Api, Resource
from ecommerce.extensions import apispec

blueprint = Blueprint("home", __name__, url_prefix="/")
api = Api(blueprint)

class HelloWorld(Resource):
    def get(self):
        return {'msg': 'Hello World'}
    
api.add_resource(HelloWorld, '/')

@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=HelloWorld, app=current_app)

