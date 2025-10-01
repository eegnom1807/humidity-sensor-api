from flask import Flask
from .db import db, migrate
from .routes import bp
import os


def create_app():
    app = Flask(__name__)

    # SQLite config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///humidity_sensor.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #initialize DB and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # register routes
    app.register_blueprint(bp, url_prefix=os.getenv("API_PREFIX", "/api/v1"))

    return app