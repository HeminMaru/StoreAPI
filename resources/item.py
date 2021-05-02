from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.itemmodel import itemModel


class all_items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM items")
        records = result.fetchall()
        items = {}
        connection.close()
        for row in records:
            items[row[0]] = {"item_id": row[0], "storeName": row[1], "itemName": row[2], "price": row[3]}
        return jsonify({"Items": items})


class sameitems(Resource):
    def get(self, itemName):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM items WHERE itemName=?", (itemName,))
        records = result.fetchall()
        items = {}
        connection.close()
        for row in records:
            items[row[1]] = {"item_id": row[0], "price": row[3]}
        return jsonify({itemName: items})


class storeitems(Resource):
    def get(self, storeName):
        if itemModel.find_store_by_name(storeName):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            result = cursor.execute("SELECT * FROM items WHERE storeName=?", (storeName,))
            records = result.fetchall()
            items = {}
            connection.close()
            for row in records:
                items[row[0]] = {"item_id": row[0], "itemName": row[2], "price": row[3]}
            return jsonify({storeName: items})
        return {"Error": "Store Not Found"}, 404


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="Price cannot be zero!")

    @jwt_required()
    def post(self, storeName, itemName):
        request_itemData = Item.parser.parse_args()
        if itemModel.find_store_by_name(storeName):
            if not itemModel.find_item_by_name(storeName, itemName):
                connection = sqlite3.connect('data.db')
                cursor = connection.cursor()
                cursor.execute("INSERT INTO items VALUES (NULL,?,?,?)", (storeName, itemName, request_itemData['price']))
                connection.commit()
                connection.close()
                return {"Item": "Item Added Successfully"}
            return {"Error": "Item Already Exist."}, 404
        return {"Error": "Store Not Found"}, 404

    def get(self, storeName, itemName):
        if itemModel.find_store_by_name(storeName):
            if itemModel.find_item_by_name(storeName, itemName):
                return itemModel.find_item_by_name(storeName, itemName)
            return {"Error": "Item Not Found"}, 404
        return {"Error": "No Store Found"}, 404

    @jwt_required()
    def put(self, storeName, itemName):
        request_itemData = Item.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        if itemModel.find_store_by_name(storeName):
            if itemModel.find_item_by_name(storeName, itemName):
                cursor.execute("UPDATE items SET price=? WHERE storeName=? AND itemName=?",
                               (request_itemData['price'], storeName, itemName))
                connection.commit()
                connection.close()
                return {"Item Found": "Updated"}
            cursor.execute("INSERT INTO items VALUES (NULL,?,?,?)", (storeName, itemName, request_itemData['price']))
            connection.commit()
            connection.close()
            return {"Item Not Found": "Created"}
        return {"Error": "Store Not Found"}, 404

    @jwt_required()
    def delete(self, storeName, itemName):
        if itemModel.find_store_by_name(storeName):
            if itemModel.find_item_by_name(storeName, itemName):
                connection = sqlite3.connect('data.db')
                cursor = connection.cursor()
                cursor.execute("DELETE FROM items WHERE storeName=? AND itemName=?", (storeName, itemName))
                connection.commit()
                connection.close()
                return {"Item": "Deleted Successfully"}
            return {"Error": "Item Not Found"}, 404
        return {"Error": "Store Not Found"}, 404
