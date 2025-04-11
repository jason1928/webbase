# app/routes/transaction_routes.py
from flask import Blueprint, request, jsonify
from app.models import transaction_model

transaction_bp = Blueprint("transaction", __name__)

@transaction_bp.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = transaction_model.get_all_transactions()
    for t in transactions:
        t["_id"] = str(t["_id"])
    return jsonify(transactions)

@transaction_bp.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.json
    result = transaction_model.create_transaction(data)
    return jsonify({"_id": str(result.inserted_id)})

@transaction_bp.route("/transactions/<transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    data = request.json
    result = transaction_model.update_transaction(transaction_id, data)
    return jsonify({"modified": result.modified_count})

@transaction_bp.route("/transactions/<transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    result = transaction_model.delete_transaction(transaction_id)
    return jsonify({"deleted": result.deleted_count})
