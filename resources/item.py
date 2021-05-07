from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.itemmodel import itemModel


class all_items(Resource):
    def get(self):
        items = {}
        for item in itemModel.query.all():
            items[item.item_id] = {"item_id": item.item_id, "storeName": item.storeName, "itemName": item.itemName, "price": item.price}
        return jsonify({"items": items})


class sameitems(Resource):
    def get(self, itemName):
        items = {}
        for item in itemModel.query.filter_by(itemName=itemName):
            items[item.storeName] = {"item_id": item.item_id, "price": item.price}
        return jsonify({itemName: items})


class storeitems(Resource):
    def get(self, storeName):
        if itemModel.find_store_by_name(storeName):
            items = {}
            for item in itemModel.query.filter_by(storeName=storeName):
                items[item.item_id] = {"item_id": item.item_id, "itemName": item.itemName, "price": item.price}
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
                item = itemModel(storeName, itemName, request_itemData['price'])
                item.insert_or_update_from_db()
                return {"Item": "Item Added Successfully"}
            return {"Error": "Item Already Exist."}, 404
        return {"Error": "Store Not Found"}, 404

    def get(self, storeName, itemName):
        if itemModel.find_store_by_name(storeName):
            if itemModel.find_item_by_name(storeName, itemName):
                return itemModel.find_item_by_name(storeName, itemName).json()
            return {"Error": "Item Not Found"}, 404
        return {"Error": "No Store Found"}, 404

    @jwt_required()
    def put(self, storeName, itemName):
        request_itemData = Item.parser.parse_args()
        if itemModel.find_store_by_name(storeName):
            item = itemModel.find_item_by_name(storeName, itemName)
            if item:
                item.price = request_itemData['price']
                item.insert_or_update_from_db()
                return {"Item found": "Updated"}
            item = itemModel(storeName, itemName, request_itemData['price'])
            item.insert_or_update_from_db()
            return {"Item not found": "Created"}
        return {"Error": "Store Not Found"}, 404

    @jwt_required()
    def delete(self, storeName, itemName):
        if itemModel.find_store_by_name(storeName):
            if itemModel.find_item_by_name(storeName, itemName):
                item = itemModel.find_item_by_name(storeName, itemName)
                item.delete_from_db()
                return {"Item": "Deleted Successfully"}
            return {"Error": "Item Not Found"}, 404
        return {"Error": "Store Not Found"}, 404
