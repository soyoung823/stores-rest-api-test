import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, JWTError

from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'young123'  # secret_key: to encode cookies
api = Api(app)

# it links them all up and allows us to call that an endpoint when it's all linked up.
# jwt enables /auth endpoint for us sending a username and password and receiving back jwt token.
jwt = JWT(app, authenticate, identity)  # /auth

# each uri will be routed to your Resource
api.add_resource(Store, '/store/<string:name>')  # uri: endpoint
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')


# whenever a disability error gets raised inside our application, (authorization header is missing)
# the auth error handler is going to be called.
@app.errorhandler(JWTError)
def auth_error_handler(err):
    return jsonify({'message': 'Could not authorize. Did you include a valid Authorization header?'}), 401


if __name__ == '__main__':
    from db import db

    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
