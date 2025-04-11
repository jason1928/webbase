# app/routes/dashboard_routes.py
from flask import Blueprint, render_template
from app.db import transaction_collection, product_collection

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    total_transaction = transaction_collection.count_documents({})
    total_users = 100  # Bisa dari user collection nanti
    total_products = product_collection.count_documents({})

    return render_template(
        "dashboard.html",
        total_transaction=total_transaction,
        total_users=total_users,
        total_products=total_products
    )
