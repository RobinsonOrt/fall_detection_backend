from Server import ma

class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('employee_id', 'name', 'last_name', 'email', 'phone', 'created_date', 'is_active', 'user_id')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)