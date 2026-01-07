from app.model.user import Users
from app import response, db
from flask import request

def singleTransform(user):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role
    }

def index():
    try:
        users = Users.query.all()
        data = [singleTransform(i) for i in users]
        return response.success(data, "Success")
    except Exception as e:
        print(e)
        return response.badRequest([], "Error")

def store():
    try:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        
        new_user = Users(name=name, email=email)
        new_user.setPassword(password)
        
        db.session.add(new_user)
        db.session.commit()
        return response.success(singleTransform(new_user), "User Created")
    except Exception as e:
        print(e)
        return response.badRequest([], "Error creating user")

def show(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user: return response.badRequest([], 'User not found')
        return response.success(singleTransform(user), "Success")
    except Exception as e:
        return response.badRequest([], "Error")

def update(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user: return response.badRequest([], 'User not found')
        
        data = request.json
        if 'name' in data: user.name = data['name']
        if 'email' in data: user.email = data['email']
        if 'password' in data: user.setPassword(data['password'])
        
        db.session.commit()
        return response.success(singleTransform(user), "User Updated")
    except Exception as e:
        return response.badRequest([], "Error")

def delete(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user: return response.badRequest([], 'User not found')
        db.session.delete(user)
        db.session.commit()
        return response.success([], "User Deleted")
    except Exception as e:
        return response.badRequest([], "Error")