from flask import Flask
from ecommerce import api
from ecommerce import auth
from ecommerce import manage
from ecommerce.extensions import apispec
from ecommerce.extensions import db
from ecommerce.extensions import jwt
from ecommerce.extensions import migrate

# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("ecommerce")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/app'
    app.config.from_object("ecommerce.config")

    if testing is True:
        app.config["TESTING"] = True
    
    configure_extensions(app)
    configure_cli(app)
    configure_apispec(app)
    register_blueprints(app)

    return app


def configure_extensions(app):
    """Configure flask extensions"""
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.init)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(api.home.blueprint)
