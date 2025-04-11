# app/models/product_model.py
from app.db import product_collection
from bson import ObjectId

def create_product(data):
    return product_collection.insert_one(data)

def get_all_products():
    return list(product_collection.find())

def get_product_by_id(product_id):
    return product_collection.find_one({"_id": ObjectId(product_id)})

def update_product(product_id, data):
    return product_collection.update_one({"_id": ObjectId(product_id)}, {"$set": data})

def delete_product(product_id):
    return product_collection.delete_one({"_id": ObjectId(product_id)})
