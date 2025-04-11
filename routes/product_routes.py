# app/routes/product_routes.py
from flask import Blueprint, request, jsonify
from app.models import product_model

product_bp = Blueprint("product", __name__)

@product_bp.route("/products", methods=["GET"])
def get_products():
    products = product_model.get_all_products()
    for p in products:
        p["_id"] = str(p["_id"])
    return jsonify(products)

@product_bp.route("/products", methods=["POST"])
def add_product():
    data = request.json
    result = product_model.create_product(data)
    return jsonify({"_id": str(result.inserted_id)})

@product_bp.route("/products/<product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.json
    result = product_model.update_product(product_id, data)
    return jsonify({"modified": result.modified_count})

@product_bp.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    result = product_model.delete_product(product_id)
    return jsonify({"deleted": result.deleted_count})
