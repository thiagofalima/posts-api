import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models.base import db


load_dotenv()

migrate = Migrate()
jwt = JWTManager()

def create_app(environment=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{environment.title()}Config")

    # initialize extensins
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # register blueprint
    from src.controllers import post, user, auth, role

    app.register_blueprint(user.pages)
    app.register_blueprint(post.pages)
    app.register_blueprint(auth.pages)
    app.register_blueprint(role.pages)

    return app
