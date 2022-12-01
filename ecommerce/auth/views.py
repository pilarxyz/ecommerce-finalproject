from flask import request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from flask_cors import CORS
from ecommerce.models import User
from ecommerce.extensions import pwd_context, jwt, apispec
from ecommerce.auth.helpers import signup_user, revoke_token, is_token_revoked, add_token_to_database


blueprint = Blueprint("auth", __name__, url_prefix="/api/v1")
CORS(blueprint)


@blueprint.route("/sign-in", methods=["POST"])
def login():
    """Authenticate user and return tokens

    ---
    post:
      tags:
        - AUTHENTICATION
      summary: Authenticate user and return tokens
      description: Authenticate user and return tokens
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  example: admin@gmail.com
                password:
                  type: string
                  example: password
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user_information:
                    type: object
                    properties:
                      email:
                        type: string
                        example:
                      name:
                        type: string
                        example:
                      phone_number:
                        type: string
                        example:
                      type:
                        type: string
                        example:
                  message:
                    type: string
                    example: Logged success
                  access_token:
                    type: string
                    example:
                  
        401:
          description: Unauthorized
    """
    
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    if user is None or not pwd_context.verify(password, user.password):
        return jsonify({"message": "Bad credentials"}), 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])


    return jsonify(
        {
            "user_information": {
                "email": user.email,
                "name": user.name,
                "phone_number": user.phone_number,
                'type': 'seller' if user.is_admin else 'buyer'
            }, 
            "message": "Login success",
            "token": access_token,
        }
    ), 200
        

@blueprint.route("/sign-up", methods=["POST"])
def register():
    """Register a user

    ---
    post:
      tags:
        - AUTHENTICATION
      summary: Register a user
      description: Register a user
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  example: pilar@gmail.com
                password:
                  type: string
                  example: password
                name:
                  type: string
                  example: Pilar Rangga Saputra 
                phone_number:
                  type: string
                  example: 088888
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: User created
                      
                  
        401:
          description: Unauthorized
    """
    
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    email = request.json.get("email", None)
    password = request.json.get("password", None)
    name = request.json.get("name", None)
    phone_number = request.json.get("phone_number", None)
    if not email or not password or not name or not phone_number:
        return jsonify({"message": "Missing email or password or name or phone_number"}), 400

    user = User.query.filter_by(email=email).first()
    if user is not None:
        return jsonify({"message": "Email already registered"}), 400
    
    user = User.query.filter_by(phone_number=phone_number).first()
    if user is not None:
        return jsonify({"message": "Phone number already registered"}), 400
      
    user = User(
        email=email,
        password=pwd_context.hash(password),
        name=name,
        phone_number=phone_number,
    )
    signup_user(user)

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])
    
    return jsonify(
        {
            "message": "success, user created",
        }
    ), 200 


@blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Get an access token from a refresh token

    ---
    post:
      tags:
        - AUTHENTICATION
      summary: Get an access token
      description: Get an access token by using a refresh token in the `Authorization` header
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: myaccesstoken
        400:
          description: bad request
        401:
          description: unauthorized
    """
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = {"access_token": access_token}
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    return jsonify(ret), 200


@blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    """Revoke an access token

    ---
    delete:
      tags:
        - AUTHENTICATION
      summary: Revoke an access token
      description: Revoke an access token
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    """Revoke a refresh token, used mainly for logout

    ---
    delete:
      tags:
        - AUTHENTICATION
      summary: Revoke a refresh token
      description: Revoke a refresh token, used mainly for logout
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@jwt.user_lookup_loader
def user_loader_callback(jwt_headers, jwt_payload):
    identity = jwt_payload["sub"]
    return User.query.get(identity)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    return is_token_revoked(jwt_payload)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=login, app=app)
    apispec.spec.path(view=register, app=app)
    apispec.spec.path(view=refresh, app=app)
    apispec.spec.path(view=revoke_access_token, app=app)
