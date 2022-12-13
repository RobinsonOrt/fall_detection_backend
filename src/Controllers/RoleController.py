from flask import jsonify

from Models.Role import Role

from Schemas.RoleSchema import role_schema, roles_schema

def list_roles():
    roles = Role.query.all()
    result = roles_schema.dump(roles)
    return jsonify(result)