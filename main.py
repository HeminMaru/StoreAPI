from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.userRegister import user_register, user_login
from resources.item import all_items, Item, sameitems, storeitems
from resources.store import all_stores, create_store
from db import db

App = Flask(__name__)
App.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
App.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
App.config['PROPAGATE_EXCEPTIONS'] = True
App.secret_key = "Hemin"
api = Api(App)


@App.before_first_request
def create_table():
    db.create_all()


jwt = JWTManager(App)


# user registration and login
api.add_resource(user_register, '/register')
api.add_resource(user_login, '/login')

# store
api.add_resource(all_stores, '/stores')
api.add_resource(create_store, '/stores/<string:ownerName>/<string:storeName>')

# item
api.add_resource(storeitems, '/stores/<string:storeName>/items')
api.add_resource(Item, '/stores/<string:storeName>/items/<string:itemName>')
api.add_resource(all_items, '/items')
api.add_resource(sameitems, '/items/<string:itemName>')
db.init_app(App)
if __name__ == '__main__':

    App.run()
