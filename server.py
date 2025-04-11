from flask import Flask, render_template

app = Flask(__name__)

# Inject menu ke semua template
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


@app.route('/')
def home():
    return render_template('dashboard.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/transaction/list')
def transaction_list():
    return render_template('transaction_list.html')


@app.route('/product/list')
def product_list():
    return render_template('product_list.html')


@app.route('/report')
def report():
    return render_template('report.html')


@app.route('/config/info')
def config_info():
    return render_template('config_info.html')


@app.route('/config/param')
def config_param():
    return render_template('config_param.html')


@app.route('/user/list')
def user_list():
    return render_template('user_list.html')


@app.route('/system/config')
def system_config():
    return render_template('system_config.html')


@app.route('/learning')
def learning_center():
    return render_template('learning_center.html')


if __name__ == '__main__':
    app.run(debug=True)
