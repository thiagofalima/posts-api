# from unittest.mock import Mocker, patch
import pytest
from src.utils import requires_role
from http import HTTPStatus


def test_requires_role_success(mocker):
    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"
    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)
    decorated_function = requires_role("admin")(lambda: "success")

    # When
    result = decorated_function()

    # Then
    assert result == "success"


def test_requires_role_failure(mocker):
    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = "error"
    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)
    decorated_function = requires_role("admin")(lambda: "success")

    # When
    result = decorated_function()

    # Then
    assert result == ({"message": "User dont have access"}, HTTPStatus.FORBIDDEN)
