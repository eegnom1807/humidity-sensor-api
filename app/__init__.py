from flask import Flask, send_from_directory, current_app
from .db import db, migrate
from .routes import register_routes
from . import models
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)

    # SQLite config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///plants_humidity_data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config["UPLOAD_FOLDER"] = os.path.join(
        BASE_DIR,
        "..",
        os.getenv("UPLOAD_FOLDER", "uploads")
    )

    #initialize DB and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # cors config
    origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    methods = os.getenv("METHODS", "GET,POST,PUT,DELETE").split(",")
    CORS(app, resources={r"/api/*": {"origins": origins, "methods": methods}})

    # register routes
    #app.register_blueprint(bp, url_prefix=os.getenv("API_PREFIX", "/api/v1"))
    register_routes(app, os.getenv("API_PREFIX", "/api/v1"))

    # serves uploaded files
    @app.route("/uploads/<path:filename>")
    def uploaded_files(filename):
        return send_from_directory(
            current_app.config["UPLOAD_FOLDER"],
            filename
        )

    return app