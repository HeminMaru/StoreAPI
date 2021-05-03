from flask import jsonify
from db import db
from models.storemodel import storeModel


class itemModel(db.Model):
    __tablename__ = 'items'

    item_id = db.Column(db.Integer, primary_key=True)
    storeName = db.Column(db.String(20))
    itemName = db.Column(db.String(100))
    price = db.Column(db.Float(precision=2))

    def __init__(self, storeName, itemName, price):
        self.storeName = storeName
        self.itemName = itemName
        self.price = price

    def json(self):
        return jsonify({"item_id": self.item_id, "storeName": self.storeName, "itemName": self.itemName, "price": self.price})

    @classmethod
    def find_item_by_name(cls, storeName, itemName):
        return cls.query.filter_by(storeName=storeName, itemName=itemName).first()

    @classmethod
    def find_store_by_name(cls, storeName):
        return storeModel.query.filter_by(storeName=storeName).first()

    def insert_or_update_from_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

