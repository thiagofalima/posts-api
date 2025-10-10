from flask import Blueprint, request, session
from src.app import Role, db
from sqlalchemy import inspect
from http import HTTPStatus
from flask_jwt_extended import jwt_required

# API RESTFull plural pattern
pages = Blueprint("role", __name__, url_prefix="/roles")

@pages.route("/", methods=["POST"])
def create_user():
    data = request.json
    role = Role(
        name=data["name"],
    )
    db.session.add(role)
    db.session.commit()
    return {"message": "Role created!"}, HTTPStatus.CREATED