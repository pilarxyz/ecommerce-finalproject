from flask import request, jsonify
from flask_restful import Resource
from ecommerce.api.schemas import ProductSchema, ProductDetailSchema
from ecommerce.models import Products, Product_Images, Images, Categories, User
from ecommerce.extensions import db, ma
from ecommerce import config
import base64
# from ecommerce.machine.main import Main

class SearchWithImages(Resource):

# request body image base64
# 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABoMA…TNE3TtPdv//vf/5Kf/3P6/woKTGyoCG/UAAAAAElFTkSuQmCC'
# response categories name and id
        # model = Main(img_input=image)

# using machine


    def post(self):
        data = request.get_json()
        image = data['image']

        model = Main(img_input=image)
        categories = model.get_categories()

        return jsonify(
            {
                'data': categories
            }
        )