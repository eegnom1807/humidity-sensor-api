from flask import Blueprint, request, jsonify
from ..models import HumidityReading
from app.schemas.dashboard_schema import dashoboard_schema
from ..db import db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/plants/dashboard", methods=["GET"])
def plants_dashboard():
    data = HumidityReading.get_plants_readings()
    message = {"data": dashoboard_schema.dump(data)}

    return jsonify(message), 200