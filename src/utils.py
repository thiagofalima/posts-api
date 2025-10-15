from flask_jwt_extended import get_jwt_identity
from src.models import User, db
from http import HTTPStatus
from functools import wraps


def requires_role(role_name):

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.get_or_404(User, user_id)

            if user.role.name != role_name:
                return {"message": "User dont have access"}, HTTPStatus.FORBIDDEN
            return f(*args, **kwargs)

        return wrapped

    return decorator
