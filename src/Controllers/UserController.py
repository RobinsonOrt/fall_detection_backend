from flask import jsonify, request
from Server import token_required, app, db
from datetime import datetime, timedelta
import bcrypt
import jwt

from Models.User import User

from Schemas.UserSchema import user_schema, users_schema

def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user is None:
        return jsonify({'response' : 'Email o contraseña incorrectos'}), 401
    if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'response' : 'Email o contraseña incorrectos'}), 401
    token = jwt.encode({
            'user_id': user.user_id,
            
            'exp' : datetime.utcnow() + timedelta(days = 7)
        }, app.config['SECRET_KEY'],
        algorithm="HS256")
    return jsonify({'token' : token, 'user_name': user.name + ' ' + user.last_name, 'role':user.role_id})

@token_required
def list_users(data):
    user = User.query.filter_by(user_id=data['user_id']).first()
    if user is None or user.role_id != 1:
        return jsonify({'response' : 'No tiene permisos para realizar esta acción'}), 401
    #get all employees where is_active = 1 and role_id = 2
    users = User.query.filter_by(is_active=1, role_id=2).all()
    result = users_schema.dump(users)
    return jsonify(result)

@token_required
def add_user(data):
    user = User.query.filter_by(user_id=data['user_id']).first()
    if user is None or user.role_id != 1:
        return jsonify({'response' : 'No tiene permisos para realizar esta acción'}), 401
    body = request.get_json()
    user = User(
        name=body['name'],
        last_name=body['last_name'],
        email=body['email'],
        password=bcrypt.hashpw(body['password'].encode('utf-8'), bcrypt.gensalt()),
        phone=body['phone'],
        created_date=datetime.utcnow(),
        is_active=True,
        role_id=2,
    )
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)

@token_required
def modify_user(data):
    user = User.query.filter_by(user_id=data['user_id']).first()
    if user is None or user.role_id != 1:
        return jsonify({'response' : 'No tiene permisos para realizar esta acción'}), 401
    body = request.get_json()
    user = User.query.get(body['user_id'])
    if user is None:
        return jsonify({'response' : 'El usuario no existe'}), 406
    user.name = body['name']
    user.last_name = body['last_name']
    user.email = body['email']
    user.phone = body['phone']
    db.session.commit()
    return user_schema.jsonify(user)

@token_required
def delete_user(data, user_id):
    user = User.query.filter_by(user_id=data['user_id']).first()
    if user is None or user.role_id != 1:
        return jsonify({'response' : 'No tiene permisos para realizar esta acción'}), 401
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'response' : 'El usuario no existe'}), 406
    user.is_active = False
    db.session.commit()
    return user_schema.jsonify(user)