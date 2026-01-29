from flask import Blueprint, request, jsonify
from ..models import HumidityReading
from ..db import db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/plants/dashboard", methods=["GET"])
def plants_dashboard():
    
    result = []
    for plant, humidity, last_reading in HumidityReading.query.all():
        result.append({
            "id": plant.id,
            "name": plant.name,
            "image_url": plant.image_url,
            "active": plant.active,
            "humidity": humidity,
            "last_reading": last_reading
        })
    
    return jsonify(result), 200