from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from login import authenticate, identity
from resources.userRegister import user_register
from resources.item import all_items, Item, sameitems, storeitems
from resources.store import all_stores, create_store
from datetime import timedelta


App = Flask(__name__)
App.secret_key = "Hemin"
api = Api(App)

App.config["JWT_AUTH_URL_RULE"] = '/login'
App.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
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

App.run()
