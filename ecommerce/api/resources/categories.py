from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ecommerce.api.schemas import CategoriesSchema
from ecommerce.models import Categories, User
from ecommerce.extensions import db, ma
from flask_cors import cross_origin

class CategoriesList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - CATEGORIES
      summary: Get all categories
      description: Get all categories
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  categories:
                    type: array
                    items: CategoriesSchema
    """

    def get(self):
        categories = db.session.execute(
            """
            SELECT categories.id, categories.title
            FROM categories
            """
        ).fetchall()

        if not categories:
          return {'message': 'Categories not found'}, 404
        
        return {'data': CategoriesSchema(many=True).dump(categories)}, 200

    def error_handler(self, error):
        return {'message': str(error)}, 400

class CategoriesDetail(Resource):
    """Creation and get_detail

    ---
    get:
      tags:
        - CATEGORIES
      summary: Get category detail
      description: Get category detail
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  categories:
                    type: array
                    items: CategoriesSchema
    """

    def get(self, id):
        category = db.session.execute(
            """
            SELECT categories.id, categories.title
            FROM categories
            WHERE categories.id = :id
            """,
            {'id': id}
        ).fetchone()
      
        if not category:
          return {'message': 'Category not found'}, 404
      
        return {'data': CategoriesSchema().dump(category)}, 200
    
    def error_handler(self, error):
        return {'message': str(error)}, 400
      
class CategoriesCreate(Resource):
    """Creation and get_detail

    ---
    post:
      tags:
        - CATEGORIES
      summary: Create category
      description: Create category
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  categories:
                    type: array
                    items: CategoriesSchema
    """

    # only admin can access this method with jwt_required
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()
        if user.is_admin:
            data = request.get_json()
            category = Categories(**data)
            db.session.add(category)
            db.session.commit()
            return {'data': 'Category added'}, 200
        else:
            return {'message': 'You are not admin'}, 401
        
    def error_handler(self, error):
        return {'message': str(error)}, 400
      
class CategoriesUpdate(Resource):
#  cross_origin() # this is for cors
    """Creation and get_detail
    
    ---
    put:
      tags:
        - CATEGORIES
      summary: Update category  
      description: Update category
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties: 
                  categories:
                    type: array
                    items: CategoriesSchema
    """
    @jwt_required()
    def put(self, id):
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()
        if user.is_admin:
            data = request.get_json()
            category = db.session.query(Categories).filter_by(id=id).first()
            category.title = data['title']
            db.session.commit()
            return {'data': 'Category updated'}, 200
        else:
            return {'message': 'You are not admin'}, 401
          
    def error_handler(self, error):
        return {'message': str(error)}, 400
    
  
      
      
      
    #     user_id = get_jwt_identity()
    #     user = db.session.query(User).filter_by(id=user_id).first()
    #     if user.is_admin:
    #         data = request.get_json()
    #         category = db.session.query(Categories).filter_by(id=id).first()
    #         if not category:
    #           return {'message': 'Category not found'}, 404
    #         category.title = data['title']
    #         db.session.commit()
    #         return {'data': 'Category updated'}, 200
    #     else:
    #         return {'message': 'You are not admin'}, 401
        
    # def error_handler(self, error):
    #     return {'message': str(error)}, 400
    
class CategoriesDelete(Resource):
    """Creation and get_detail

    ---
    delete:
      tags:
        - CATEGORIES
      summary: Delete category
      description: Delete category
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  categories:
                    type: array
                    items: CategoriesSchema
    """

    # only admin can access this method with jwt_required
    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()
        if user.is_admin:
            category = db.session.query(Categories).filter_by(id=id).first()
            if not category:
              return {'message': 'Category not found'}, 404
            db.session.delete(category)
            db.session.commit()
            return {'data': 'Category deleted'}, 200
        else:
            return {'message': 'You are not admin'}, 401
        
    def error_handler(self, error):
        return {'message': str(error)}, 400

      
      
      
# class CategoriesCreate(Resource):
#     """Creation and get_detail

#     ---
#     post:
#       tags:
#         - CATEGORIES
#       summary: Create new category
#       description: Create new category
#       requestBody:
#         content:
#           application/json:
#             schema:
#               type: object
#               properties: 
#                 title:
#                   type: string
#       responses:
#         200:
#           content:
#             application/json:
#               schema:
#                 type: object
#                 properties:
#                   categories:
#                     type: array
#                     items: CategoriesSchema
#     """
#     @jwt_required()
#     def post(self):
#         data = request.get_json()
#         category = Categories(
#             title=data['title']
#         )
#         db.session.add(category)
#         db.session.commit()
#         return {'message': 'Category added'}, 200

#     def error_handler(self, error):
#         return {'message': str(error)}, 400
  
# class CategoriesUpdate(Resource):
#     """Creation and get_detail

#     ---
#     put:
#       tags:
#         - CATEGORIES
#       summary: Update category
#       description: Update category
#       requestBody:
#         content:
#           application/json:
#             schema:
#               type: object
#               properties: 
#                 title:
#                   type: string
#       responses:
#         200:
#           content:
#             application/json:
#               schema:
#                 type: object
#                 properties:
#                   categories:
#                     type: array
#                     items: CategoriesSchema
#     """
#     def put(self, id):
#         data = request.get_json()
#         category = db.session.execute(
#             """
#             SELECT categories.id, categories.title
#             FROM categories
#             WHERE categories.id = :id
#             """,
#             {'id': id}
#         ).fetchone()
      
#         if not category:
#           return {'message': 'Category not found'}, 404
      
#         category = Categories.query.get(id)
#         category.title = data['title']
      
#         db.session.commit()
      
#         return {'message': 'Category updated'}, 200
    
#     def error_handler(self, error):
#         return {'message': str(error)}, 400
      
# class CategoriesDelete(Resource):
#     """Creation and get_detail

#     ---
#     delete:
#       tags:
#         - CATEGORIES
#       summary: Delete category
#       description: Delete category
#       responses:
#         200:
#           content:
#             application/json:
#               schema:
#                 type: object
#                 properties:
#                   categories:
#                     type: array
#                     items: CategoriesSchema
#     """
    
#     @jwt_required()
#     def delete(self, id):
#         category = db.session.execute(
#             """
#             SELECT categories.id, categories.title
#             FROM categories
#             WHERE categories.id = :id
#             """,
#             {'id': id}
#         ).fetchone()
      
#         if not category:
#           return {'message': 'Category not found'}, 404
      
#         category = Categories.query.get(id)
      
#         db.session.delete(category)
        
#         db.session.commit()
      
#         return {'message': 'Category deleted'}, 200
    
#     def error_handler(self, error):
#         return {'message': str(error)}, 400