from http import HTTPStatus
from src.models import Role, db


def test_create_role(client):

    # Given
    payload = {
        "name": "admin",
    }

    # When
    response = client.post("/roles/", json=payload)

    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "Role created!"}


def test_list_roles(client):

    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    # When
    response = client.get("/roles/")

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "roles": [
            {
                "id": role.id,
                "name": role.name,
            }
        ]
    }


def test_get_role_success(client):
    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    # When
    response = client.get(f"/roles/{role.id}")

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": role.id,
        "name": role.name,
    }


def test_get_role_not_found(client):
    # Given
    role_id = 1

    # When
    response = client.get(f"/roles/{role_id}")

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == None
