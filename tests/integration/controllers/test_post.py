from http import HTTPStatus
from src.app import Post, db
from sqlalchemy import func


def test_create_post(client):

    # Given
    payload = {"title": "test", "body": "test", "author_id": 1}

    # When
    response = client.post("/posts/", json=payload)

    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "Post created!"}


def test_list_posts(client):

    # Given
    post = Post(title="title", body="body", author_id="author_id")
    db.session.add(post)
    db.session.commit()

    # When
    response = client.get("/posts/")

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "body": post.body,
                "created": post.created.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "author_id": post.author_id,
            }
        ]
    }


def test_get_post_success(client):
    # Given
    post = Post(title="title", body="body", author_id="author_id")
    db.session.add(post)
    db.session.commit()

    # When
    response = client.get(f"/posts/{post.id}")

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "author_id": post.author_id,
    }


def test_get_post_not_found(client):
    # Given
    post_id = 1

    # When
    response = client.get(f"/posts/{post_id}")

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == None
