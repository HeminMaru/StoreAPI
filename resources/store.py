from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.usermodel import userModel
from models.storemodel import storeModel
from models.itemmodel import itemModel


class all_stores(Resource):
    def get(self):
        stores = {}
        for store in storeModel.query.all():
            stores[store.ownerName] = {"store_id": store.store_id, "ownerName": store.ownerName, "storeName": store.storeName}
        return jsonify({"stores": stores})


class create_store(Resource):
    @jwt_required()
    def post(self, ownerName, storeName):
        if userModel.find_by_username(ownerName):
            store = storeModel.find_store_by_name_and_ownerName(storeName, ownerName)
            if store:
                return {"Error": "Store Already exist"}, 400
            store = storeModel(ownerName, storeName)
            store.create_store()
            return {"Store": "Added Successfully"}
        return {"Error": "Owner is not registered."}

    @jwt_required()
    def delete(self, ownerName, storeName):
        if userModel.find_by_username(ownerName):
            store = storeModel.find_store_by_name_and_ownerName(storeName, ownerName)
            if store:
                for item in itemModel.query.filter_by(storeName=storeName):
                    item.delete_from_db()
                store.delete_store_and_items()
                return {"Store": "Deleted Successfully"}
            return {"Error": "Store Not Found"}, 404
        return {"Error": "Owner is not registered"}

    def get(self, ownerName, storeName):
        if userModel.find_by_username(ownerName):
            if storeModel.find_store_by_name_and_ownerName(storeName, ownerName):
                return storeModel.find_store_by_name_and_ownerName(storeName, ownerName).json()
            return {"Error": "Store Not Found"}, 404
        return{"Error": "Owner is not registered"}


