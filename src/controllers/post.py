from flask import Blueprint, request, session, jsonify
from src.app import Post, db
from sqlalchemy import inspect
from http import HTTPStatus

pages = Blueprint("post", __name__, url_prefix="/posts")


def create_post():
    data = request.json
    post = Post(title=data["title"], body=data["body"], author_id=data["author_id"])
    db.session.add(post)
    db.session.commit()


def list_posts():

    results = db.session.execute(db.select(Post)).scalars().all()
    return [
        {
            "id": result.id,
            "title": result.title,
            "body": result.body,
            "created": result.created,
            "author_id": result.author_id,
        }
        for result in results
    ]


@pages.route("/", methods=["GET", "POST"])
def handle_post():

    if request.method == "POST":
        try:
            create_post()
            return {"message": "Post created!"}, HTTPStatus.CREATED
        except ValueError as e:
            return {"error": str(e)}, HTTPStatus.BAD_REQUEST

    else:
        return {"posts": list_posts()}, HTTPStatus.OK


@pages.route("/<int:post_id>", methods=["GET"])
def get_post_by_id(post_id):
    post = db.get_or_404(Post, post_id)
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created,
        "author_id": post.author_id,
    }


@pages.route("/<int:post_id>", methods=["GET", "PATCH"])
def update_post_by_id(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()

    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created,
        "author_id": post.author_id,
    }


@pages.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
