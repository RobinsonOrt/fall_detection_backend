from Server import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'name', 'last_name', 'email', 'password', 'phone', 'created_date', 'is_active', 'role_id')

user_schema = UserSchema()
users_schema = UserSchema(many=True)