import sqlite3
from flask import jsonify


class storeModel:
    def __init__(self, ownerName, storeName):
        self.ownerName = ownerName
        self.storeName = storeName

    def json(self):
        return jsonify({"ownerName": self.ownerName, "storeName": self.storeName})

    @classmethod
    def find_store_by_name_and_ownerName(cls, storeName, ownerName):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM stores WHERE storeName=?  AND ownerName=?", (storeName, ownerName))
        row = result.fetchone()
        connection.close()
        if row:
            return jsonify({"Store": {"store_id": row[0], "ownerName": row[1], "storeName": row[2]}})
        return
