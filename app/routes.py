from app import app
from flask import request, make_response, jsonify
from app.database import getUserByUsername, setNewPendingUser, getPendingUser, registerUser, getEvents
from app.decorators import token_required
import jwt
import datetime

from werkzeug.security import generate_password_hash, check_password_hash
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

    return doLogin(username, password)


def doLogin(username, password):
    if username is None or password is None:
        return make_response('Username and password required!', 401)

    userData = getUserByUsername(username, False)
    if userData is not None and userData[1] == username and check_password_hash(userData[2], password):
        # todo https://flask-jwt-extended.readthedocs.io/en/stable/refresh_tokens/
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        }, app.config['SECRET_KEY'])
        # todo return encrypted seed
        return jsonify({'access_token': token.decode('UTF-8'), 'seed': userData[3]})

    return make_response('Invalid username or password!', 401)


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


@app.route('/checkHash', methods=['POST'])
def checkHash():
    req = request.get_json()
    hash = None
    if 'hash' in req:
        hash = req['hash']
    if hash is not None:
        userData = getPendingUser(hash)
        if userData is not None:
            return 'success'
        else:
            return make_response('User not found', 401)

    return make_response('User not found', 401)


@app.route('/register', methods=['POST'])
def register():
    req = request.get_json()
    hash = None
    password = None
    seed = None
    if 'hash' in req and 'password' in req:
        hash = req['hash']
        password = req['password']
        seed = req['seed']
    if hash is not None and password is not None and seed is not None:
        userData = getPendingUser(hash)
        if userData is not None:
            registerUser(password, str(hash), seed)
            return doLogin(userData[1], password)

    return make_response('User not found', 401)


@app.route('/events')
def events():
    data = getEvents()
    return jsonify(data)


@app.route('/auth')
@token_required
def auth():
    return 'success'
