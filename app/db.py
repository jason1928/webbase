# app/db.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["web_dashboard_db"]

product_collection = db["products"]
transaction_collection = db["transactions"]
