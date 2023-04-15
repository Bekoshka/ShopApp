import db_session
from model.user import User
from flask import request, Response, jsonify, make_response
from core import app


@app.post('/users')
def create_user():
    user = User(**request.json)
    db_session.add(user)
    db_session.commit()
    return user.id


@app.get('/users')
def get_user():
    return User.items()






