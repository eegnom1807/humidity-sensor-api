from flask import Blueprint, jsonify, request
from ..models import Sensor
from ..utils import get_date
from ..db import db

sensors_bp = Blueprint("sensors", __name__)


@sensors_bp.route("/sensors", methods=["GET"])
def get_all_sensors():
    sensors = []
    data = Sensor.get_all()

    for row in data:
        sensors.append({
            "id": row.id,
            "pin": row.pin,
            "plant_id": row.plant_id,
            "created_at": get_date(row.created_at),
            "updated_at": get_date(row.updated_at)
        })

    return jsonify(sensors), 200

@sensors_bp.route("/sensors", methods=["POST"])
def add_sensor():
    data = request.json
    
    sensor = Sensor(
        pin=data["pin"],
        plant_id=data["plant_id"]
    )

    try:
        db.session.add(sensor)
        db.session.commit()
    except:
        db.session.rollback()
        error = {"message": "Conflict"}
        return error, 409
    
    message = {"message": "Created"}
    return jsonify(message), 201

@sensors_bp.route("/sensors/<int:id>", methods=["GET"])
def get_sensor_by_id(id):
    data = Sensor.get_by_id(id)
    if data is None:
        error = {"message":  "Not Found"}
        return error, 404
    
    sensor = {
        "id": data.id,
        "pin": data.pin,
        "plant_id": data.plant_id,
        "created_at": get_date(data.created_at),
        "updated_at": get_date(data.updated_at)
    }

    return jsonify(sensor), 200

@sensors_bp.route("/sensors/<int:id>", methods=["PUT"])
def update_sensor(id):
    sensor = Sensor.get_by_id(id)
    if sensor is None:
        error = {"message":  "Not Found"}
        return error, 404
    
    new_data = request.json
    sensor.pin = new_data["pin"]
    sensor.plant_id = new_data["plant_id"]

    try:
        db.session.commit()
    except:
        db.session.rollback()
        error = {"message":  "Conflict"}
        return error, 409
    
    return {}, 204

@sensors_bp.route("/sensors/<int:id>", methods=["DELETE"])
def delete_sensor(id):
    sensor = Sensor.get_by_id(id)
    if sensor is None:
        error = {"message":  "Not Found"}
        return error, 404

    try:
        db.session.delete(sensor)
        db.session.commit()
    except:
        db.session.rollback()
        error = {"message":  "Conflict"}
        return error, 409
    
    return {}, 200