from flask import Flask
from .extensions import db, migrate, login_manager, init_user_loader

from .models.models import User
from flask import render_template, redirect, url_for, request

# import routes
from .routes.auth import auth
from .routes.user import user

def create_app():
    app = Flask(__name__, template_folder="views")

    app.config.from_object("config.DevelopmentConfig")

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    init_user_loader(User)

    @app.route("/")
    def home():
        return render_template("home.html")

    app.register_blueprint(auth)
    app.register_blueprint(user)

    return app
