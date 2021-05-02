from flask import jsonify
from flask_restful import Resource
from flask_jwt import jwt_required
import sqlite3
from models.usermodel import userModel
from models.storemodel import storeModel


class all_stores(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM stores")
        records = result.fetchall()
        connection.close()
        stores = {}
        for row in records:
            stores[row[0]] = {"store_id": row[0], "ownerName": row[1], "storeName": row[2]}
        return jsonify({"stores": stores})


class create_store(Resource):
    @jwt_required()
    def post(self, ownerName, storeName):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        if ownerName.find_by_username():
            if not storeModel.find_store_by_name_and_ownerName(storeName, ownerName):
                cursor.execute("INSERT INTO stores VALUES (NULL,?,?)", (ownerName, storeName))
                connection.commit()
                connection.close()
                return {"Store": "Added Successfully"}
            return {"Error": "Store Already exist"}, 400
        return {"Error": "Owner is not registered."}

    @jwt_required()
    def delete(self, ownerName, storeName):
        if storeModel.find_store_by_name_and_ownerName(storeName, ownerName):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM stores WHERE storeName=? AND ownerName=?", (storeName, ownerName))
            cursor.execute("DELETE FROM items WHERE storeName=?", (storeName,))
            connection.commit()
            connection.close()
            return {"Store": "Deleted Successfully"}
        return {"Error": "Store Not Found"}, 404

    def get(self, ownerName, storeName):
        if storeModel.find_store_by_name_and_ownerName(storeName, ownerName):
            return storeModel.find_store_by_name_and_ownerName(storeName, ownerName)
        return {"Error": "Store Not Found"}, 404


