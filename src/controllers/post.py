from flask import Blueprint, request, session, jsonify
from src.app import Post, db
from sqlalchemy import inspect
from http import HTTPStatus

pages = Blueprint("post", __name__, url_prefix="/posts")

def create_post():
    data = request.json
    post = Post(
        title=data["title"],
        body=data["body"],
        author_id=data["author_id"]
    )
    db.session.add(post)
    db.session.commit()


def list_posts():
    
    results = db.session.execute(db.select(Post)).scalars().all()
    return [
        {"id": result.id,
         "title": result.title,
         "body": result.body,
         "created": result.created,
         "author_id": result.author_id
        }
        for result in results
    ]

@pages.route("/", methods=["GET", "POST"])
def handle_post():

    if request.method == "POST":
        try:
            create_post()
            return {"mssage": "Post created!"}, HTTPStatus.CREATED
        except ValueError as e:
            return {"error": str(e)}, HTTPStatus.BAD_REQUEST
    
    else:
        return {"posts": list_posts()}, HTTPStatus.OK
    
