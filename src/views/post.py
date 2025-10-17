from src.app import ma
from src.models import Post

class PostSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Post

    id = ma.auto_field()
    title = ma.auto_field()
    body = ma.auto_field()
    created = ma.auto_field()
    author_id = ma.auto_field()
