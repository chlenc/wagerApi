from app import app
from flask import request,  jsonify
from functools import wraps
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'token is missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'invalid token'}), 403

        return f(*args, **kwargs)

    return decorated