from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Koneksi MongoDB lokal
client = MongoClient("mongodb://localhost:27017/")
db = client["web_dashboard_db"]
collection = db["users_db"]


# Inject menu ke semua halaman
@app.context_processor
def inject_menus():
    menus = [
        ("Home", "/dashboard"),
        ("Transaction", "/transaction/list"),
        ("Product", "/product/list"),
        ("Report", "/report"),
        ("Config Information", "/config/info"),
        ("Parameter Setting", "/config/param"),
        ("User Management", "/user/list"),
        ("System Config", "/system/config"),
        ("Learning Center", "/learning")
    ]
    return dict(menus=menus)


@app.route("/")
@app.route("/dashboard")
def dashboard():
    users = collection.find()
    return render_template("dashboard.html", users=users)


@app.route("/transaction/list")
def transaction_list():
    return render_template("transaction_list.html")


@app.route("/product/list")
def product_list():
    return render_template("product_list.html")


@app.route("/report")
def report():
    return render_template("report.html")


@app.route("/config/info")
def config_info():
    return render_template("config_info.html")

@app.route("/config/param")
def config_param():
    return render_template("config_param.html")


@app.route("/user/list")
def user_list():
    users = list(collection.find())  # Ganti dari users_db ke collection
    return render_template("user_list.html", users=users)




@app.route("/system/config")
def system_config():
    return render_template("system_config.html")


@app.route("/learning")
def learning_center():
    return render_template("learning_center.html")


if __name__ == "__main__":
    app.run(debug=True)