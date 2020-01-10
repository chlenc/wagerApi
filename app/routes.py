from app import app
from flask import request, make_response, jsonify
from app.database import getUserByUsername, setNewPendingUser
from app.decorators import token_required
import jwt
import datetime

# from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import randomString, sendEmailWithLink


@app.route('/login', methods=['POST'])
def login():
    req = request.get_json()
    username = None
    password = None
    # remember = None
    if 'username' in req and 'password' in req:
        username = req['username']
        password = req['password']

    if username is None or password is None:
        return make_response('Username and password required!', 401,
                             {'WWW-Authenticate': 'Basic realm="Login Required"'})

    userData = getUserByUsername(username, False)
    if userData is not None and userData[1] == username and userData[2] == password:
        # check_password_hash(userData[1], password):
        # todo https://flask-jwt-extended.readthedocs.io/en/stable/refresh_tokens/
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        }, app.config['SECRET_KEY'])
        return jsonify({'access_token': token.decode('UTF-8')})

    return make_response('Invalid username or password!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/checkUser', methods=['POST'])
def checkUser():
    req = request.get_json()
    username = None
    if 'username' in req:
        username = req['username']
    if username is not None:
        userData = getUserByUsername(username, False)
        if userData is not None:
            return 'success'

    return make_response('Invalid username!', 401)


@app.route('/registerReq', methods=['POST'])
def registerReq():
    req = request.get_json()
    username = None
    if 'username' in req:
        username = req['username']
    if username is not None:
        userData = getUserByUsername(username, True)
        if userData is None:
            pendingHash = randomString()
            success = sendEmailWithLink(username, pendingHash)
            if success:
                setNewPendingUser(username, pendingHash)
                return 'success'
            else:
                return make_response('Something wrong!', 403)

    return make_response('User already exists!', 403)


@app.route('/auth')
@token_required
def auth():
    return 'success'
