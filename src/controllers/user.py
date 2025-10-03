from flask import Blueprint, request, session
from src.app import User, db
from dataclasses import asdict
from http import HTTPStatus

# API RESTFull plural pattern
pages = Blueprint("user", __name__, url_prefix="/users")

def create_user():
    data = request.json
    user = User(
        username=data["username"],
    )
    db.session.add(user)
    db.session.commit()


@pages.route("/", methods=["GET", "POST"])
def hendle_user():
    
    if request.method == "POST":
        create_user()
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        return {"users": []}, HTTPStatus.OK
    



