from flask import jsonify
from db import db

class storeModel(db.Model):
    __tablename__ = 'stores'

    store_id = db.Column(db.Integer, primary_key=True)
    ownerName = db.Column(db.String(20))
    storeName = db.Column(db.String(40))

    def __init__(self, ownerName, storeName):
        self.ownerName = ownerName
        self.storeName = storeName

    def json(self):
        return jsonify({"store_id": self.store_id, "ownerName": self.ownerName, "storeName": self.storeName})

    @classmethod
    def find_store_by_name_and_ownerName(cls, storeName, ownerName):
        return cls.query.filter_by(storeName=storeName, ownerName=ownerName).first()

    def delete_store_and_items(self):
        db.session.delete(self)
        db.session.commit()

    def create_store(self):
        db.session.add(self)
        db.session.commit()
