from flask import Blueprint, request
from src.models import Role, db
from http import HTTPStatus
from src.views import RoleSchema

# API RESTFull plural pattern
pages = Blueprint("role", __name__, url_prefix="/roles")

def create_role():
    data = request.json
    role = Role(
        name=data["name"],
    )
    db.session.add(role)
    db.session.commit()


def list_roles():
    query = db.select(Role)
    roles = db.session.execute(query).scalars().all()
    roles_schema = RoleSchema(many=True)
    return roles_schema.dump(roles)

@pages.route("/", methods=["GET","POST"])
def handle_roles():
    if request.method == "POST":
        try:
            create_role()
            return {"message": "Role created!"}, HTTPStatus.CREATED
        except ValueError as e:
            return {"error": str(e)}, HTTPStatus.BAD_REQUEST
    else:
        return {"roles": list_roles()}, HTTPStatus.OK
    
@pages.route("/<int:role_id>", methods=["GET"])
def get_user_by_id(role_id):
    role = db.get_or_404(Role, role_id)
    role_schema = RoleSchema()
    return role_schema.dumps(role)