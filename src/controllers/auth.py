from flask import Blueprint, request, session
from src.app import User, db
from sqlalchemy import inspect
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required

# API RESTFull plural pattern
pages = Blueprint("auth", __name__, url_prefix="/auth")

@pages.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if not user or user.password != password:
        return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token}