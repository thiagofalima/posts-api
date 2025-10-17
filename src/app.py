import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models.base import db
from flask_bcrypt import Bcrypt
from flask import json
from werkzeug.exceptions import HTTPException
from flask_marshmallow import Marshmallow


load_dotenv()

migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()

def create_app(environment="Development"):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{environment.title()}Config")

    # initialize extensins
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    # register blueprint
    from src.controllers import post, user, auth, role

    app.register_blueprint(user.pages)
    app.register_blueprint(post.pages)
    app.register_blueprint(auth.pages)
    app.register_blueprint(role.pages)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    return app
