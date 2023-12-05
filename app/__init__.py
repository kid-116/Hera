from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask_login import LoginManager

from config import Config

from app.utils.oidc_client import WSO2Client

def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    mysql = MySQL(app)
    app.config['DATABASE_CONN'] = mysql

    login = LoginManager(app)
    login.login_view = 'index'
    app.config['LOGIN'] = login

    app.config['IS_CLIENT'] = WSO2Client(
        app.config['WSO2_CLIENT_ID'],
        app.config['WSO2_CLIENT_SECRET'],
        app.config['WSO2_HOST']
    )

    with app.app_context():
        from .users import users
        from .dash import dash
        from .transactions import transactions

        app.register_blueprint(users.users_bp)
        app.register_blueprint(dash.dash_bp)
        app.register_blueprint(transactions.transactions_bp)

        @app.route('/')
        def index():
            return render_template('home.html')

        @app.route('/about')
        def about():
            return render_template('about.html')

        return app
