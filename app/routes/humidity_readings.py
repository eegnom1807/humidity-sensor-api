from flask import Blueprint, request, jsonify
from ..models import HumidityReading, Sensor
from ..utils import require_api_key
from ..db import db

readings_bp = Blueprint("readings", __name__)


@readings_bp.route("/readings", methods=["POST"])
def create_reading():
    require_api_key()

    data = request.json
    pin = data["pin"]
    humidity = data["humidity"]
    if pin is None or humidity is None:
        return {"error": "pin and humidity required"}, 400

    sensor = Sensor.get_by_pin(pin)
    if not sensor:
        return {"error": "Sensor not found"}, 404

    reading = HumidityReading(
        sensor_id=sensor.id,
        humidity=humidity
    )

    db.session.add(reading)

    # active plant
    if not sensor.plant.active:
        sensor.plant.active = True

    db.session.commit()

    message = {"status": "ok"}
    return jsonify(message), 201