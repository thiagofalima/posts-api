from flask import Blueprint, request
from src.models import User, db
from sqlalchemy import inspect
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from src.utils import requires_role
from src.app import bcrypt
from src.views import UserSchema

# API RESTFull plural pattern
pages = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    data = request.json
    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]),
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    users_schema = UserSchema(many=True)
    return users_schema.dump(users)



@pages.route("/", methods=["GET", "POST"])
# @jwt_required()
# @requires_role("admin")
def hendle_user():
    
    if request.method == "POST":
        try:
            _create_user()
            return {"message": "User created!"}, HTTPStatus.CREATED
        except ValueError as e:
            return {"error": str(e)}, HTTPStatus.BAD_REQUEST
    else:
        return {"users": _list_users()}, HTTPStatus.OK


@pages.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = db.get_or_404(User, user_id)
    user_schema = UserSchema()
    return user_schema.dumps(user)


# For partial updates, PATCH
@pages.route("/<int:user_id>", methods=["GET", "PATCH"])
def update_user_by_id(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()
    user_schema = UserSchema()
    return user_schema.dump(user)


@pages.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
