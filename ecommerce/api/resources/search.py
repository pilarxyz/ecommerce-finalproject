from flask import request, jsonify
from flask_restful import Resource
from ecommerce.api.schemas import ProductSchema, ProductDetailSchema
from ecommerce.models import Products, Product_Images, Images, Categories, User
from ecommerce.extensions import db, ma
from ecommerce import config
import base64
import ecommerce.machine_learning.initialization as ml

class SearchWithImages(Resource):

# request body image base64
# 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABoMA…TNE3TtPdv//vf/5Kf/3P6/woKTGyoCG/UAAAAAElFTkSuQmCC'
# response categories name and id

# using machine learning


    def post(self):
        data = request.get_json()
        image = data['image']
        image = image.split(',')[1]
        image = base64.b64decode(image)
        image = ml.
