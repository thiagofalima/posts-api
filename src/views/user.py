from src.app import ma
from src.models import User
from .role import RoleSchema

class UserSchema(ma.SQLAlchemySchema):

    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    role = ma.Nested(RoleSchema)
