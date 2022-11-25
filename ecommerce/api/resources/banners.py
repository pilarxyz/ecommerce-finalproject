from flask import request
from flask_restful import Resource

from ecommerce.api.schemas import BannerSchema
from ecommerce.models import Banners
from ecommerce.extensions import db, ma
    
class BannerList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - home
      summary: Get all banners
      description: Get all banners
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  banners:
                    type: array
                    items: BannerSchema
    """

    def get(self):
        banners = Banners.query.all()
        return {'data': BannerSchema(many=True).dump(banners)}, 200
    
    def error_handler(self, error):
        return {'message': str(error)}, 400