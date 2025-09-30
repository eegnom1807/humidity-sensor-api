from flask import Flask
from .extensions import db, migrate
from .routes import bp


def create_app():
    app = Flask(__name__)

    # SQLite config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///humidity_sensor.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #initialize DB and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # register routes
    app.register_blueprint(bp)

    return app