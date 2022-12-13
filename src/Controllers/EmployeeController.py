from flask import jsonify, request
from Server import token_required, db
from datetime import datetime, timedelta

from Models.Employee import Employee
from Models.User import User

from Schemas.EmployeeSchema import employee_schema, employees_schema

@token_required
def list_employees(data):
    user = User.query.filter_by(user_id=data['user_id']).first()
    if user is None or user.role_id != 1:
        return jsonify({'response' : 'No tiene permisos para realizar esta acción'}), 401
    #get all employees where is_active = 1
    employees = Employee.query.filter_by(is_active=1).all()
    result = employees_schema.dump(employees)
    return jsonify(result)

@token_required
def add_employee(data):
    user = User.query.filter_by(user_id=data['user_id']).first()
    if user is None or user.role_id != 1:
        return jsonify({'response' : 'No tiene permisos para realizar esta acción'}), 401
    body = request.get_json()
    employee = Employee(
        name=body['name'],
        last_name=body['last_name'],
        email=body['email'],
        phone=body['phone'],
        created_date=datetime.utcnow(),
        is_active=True,
        user_id=user.user_id
    )
    db.session.add(employee)
    db.session.commit()
    return employee_schema.jsonify(employee)

@token_required
def modify_employee(data):
    user = User.query.filter_by(user_id=data['user_id']).first()
    if user is None or user.role_id != 1:
        return jsonify({'response' : 'No tiene permisos para realizar esta acción'}), 401
    body = request.get_json()
    employee = Employee.query.get(body['employee_id'])
    if employee is None:
        return jsonify({'response' : 'El empleado no existe'}), 406
    employee.name = body['name']
    employee.last_name = body['last_name']
    employee.email = body['email']
    employee.phone = body['phone']
    db.session.commit()
    return employee_schema.jsonify(employee)


@token_required
def delete_employee(data, employee_id):
    user = User.query.filter_by(user_id=data['user_id']).first()
    if user is None or user.role_id != 1:
        return jsonify({'response' : 'No tiene permisos para realizar esta acción'}), 401
    employee = Employee.query.get(employee_id)
    if employee is None:
        return jsonify({'response' : 'El empleado no existe'}), 406
    employee.is_active = False
    db.session.commit()
    return employee_schema.jsonify(employee)

def get_employee_phones():
    employees = Employee.query.filter_by(is_active=1).all()
    result = employees_schema.dump(employees)
    #conver to a iterable objec
    return result