from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'

from app import routes
