from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from login import authenticate, identity
from resources.userRegister import user_register
from resources.item import all_items, Item, sameitems, storeitems
from resources.store import all_stores, create_store
from db import db

App = Flask(__name__)
App.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
App.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
App.secret_key = "Hemin"
api = Api(App)


@App.before_first_request
def create_table():
    db.create_all()


App.config["JWT_AUTH_URL_RULE"] = '/login'
jwt = JWT(App, authenticate, identity)


# user registration
api.add_resource(user_register, '/register')

# store
api.add_resource(all_stores, '/stores')
api.add_resource(create_store, '/stores/<string:ownerName>/<string:storeName>')

# item
api.add_resource(storeitems, '/stores/<string:storeName>/items')
api.add_resource(Item, '/stores/<string:storeName>/items/<string:itemName>')
api.add_resource(all_items, '/items')
api.add_resource(sameitems, '/items/<string:itemName>')

if __name__ == '__main__':
    db.init_app(App)
    App.run()
