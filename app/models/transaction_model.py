# app/models/transaction_model.py
from app.db import transaction_collection
from bson import ObjectId

def create_transaction(data):
    return transaction_collection.insert_one(data)

def get_all_transactions():
    return list(transaction_collection.find())

def get_transaction_by_id(transaction_id):
    return transaction_collection.find_one({"_id": ObjectId(transaction_id)})

def update_transaction(transaction_id, data):
    return transaction_collection.update_one({"_id": ObjectId(transaction_id)}, {"$set": data})

def delete_transaction(transaction_id):
    return transaction_collection.delete_one({"_id": ObjectId(transaction_id)})
