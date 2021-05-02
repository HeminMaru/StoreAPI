import sqlite3
from flask import jsonify


class itemModel:
    def __init__(self, itemName, storeName):
        self.itemName = itemName
        self.storeName = storeName

    def json(self):
        return jsonify({"storeName": self.storeName, "itemName": self.itemName})

    @classmethod
    def find_item_by_name(cls, storeName, itemName):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM items WHERE storeName=? and itemName=?", (storeName, itemName))
        row = result.fetchone()
        connection.close()
        if row:
            return jsonify({"Item": {"item_id": row[0], "storeName": row[1], "itemName": row[2], "price": row[3]}})
        return

    @classmethod
    def find_store_by_name(cls, storeName):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM stores WHERE storeName=?", (storeName,))
        row = result.fetchone()
        connection.close()
        if row:
            return jsonify({"Store": {"store_id": row[0], "ownerName": row[1], "storeName": row[2]}})
        return

