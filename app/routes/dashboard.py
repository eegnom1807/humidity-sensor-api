from flask import Blueprint, request, jsonify
from ..models import HumidityReading
from ..db import db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/plants/dashboard", methods=["GET"])
def plants_dashboard():
    readings = []
    data = HumidityReading.get_plants_readings()
    for row in data:
        readings.append({
            "id": row.id,
            "name": row.name,
            "image_url": row.image_url,
            "active": row.active,
            "humidity": row.humidity,
            "last_reading": row.last_reading
        })
    
    return jsonify(readings), 200