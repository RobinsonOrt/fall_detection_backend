from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from functools import wraps
from flask_cors import CORS
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = ''#insert secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@'#complete the db url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'response' : 'No se encuentra el token'}), 401
        
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        except:
            return jsonify({
                'message' : 'Token invalido'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(data, *args, **kwargs)
  
    return decorated
