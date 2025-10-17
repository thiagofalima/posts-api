from flask import Blueprint, request
from src.models import Post, db
from sqlalchemy import inspect
from http import HTTPStatus
from src.views import PostSchema

pages = Blueprint("post", __name__, url_prefix="/posts")


def create_post():
    data = request.json
    post = Post(title=data["title"], body=data["body"], author_id=data["author_id"])
    db.session.add(post)
    db.session.commit()


def list_posts():

    posts = db.session.execute(db.select(Post)).scalars().all()
    posts_schema = PostSchema(many=True)
    return posts_schema.dump(posts)


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
    post_schema = PostSchema()
    return post_schema.dump(post)


@pages.route("/<int:post_id>", methods=["GET", "PATCH"])
def update_post_by_id(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()
    
    post_schema = PostSchema()
    return post_schema.dump(post)


@pages.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
