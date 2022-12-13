from Server import ma

class RoleSchema(ma.Schema):
    class Meta:
        fields = ('role_id', 'role_name', 'role_description')

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)