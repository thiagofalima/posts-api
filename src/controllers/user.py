from flask import Blueprint, request, session
from src.app import User, db
from dataclasses import asdict
from sqlalchemy import inspect
from http import HTTPStatus

# API RESTFull plural pattern
pages = Blueprint("user", __name__, url_prefix="/users")

def _create_user():
    data = request.json
    user = User(
        username=data["username"],
    )
    db.session.add(user)
    db.session.commit()

def _list_users():
    query = db.select(User)
    results =  db.session.execute(query).scalars().all()
    return [
        {"id": result.id,
         "username": result.username
        }
        for result in results
    ]

@pages.route("/", methods=["GET", "POST"])
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
    return {
        "id": user.id,
        "username": user.username
    }


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
    
    

    return {
        "id": user.id,
        "username": user.username
    }

@pages.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return {"message": f"User {user.username} deleted!!"}, HTTPStatus.NO_CONTENT
