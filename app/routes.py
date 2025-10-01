from flask import Blueprint, jsonify, request
from .models import HumiditySensor
from .db import db

bp = Blueprint("api", __name__)


@bp.route("/humidity-sensor", methods=["GET"])
def get_all_humidity_sensor():
    result = HumiditySensor.query.all()
    return jsonify([r.to_dict() for r in result]), 200

@bp.route("/humidity-sensor/<int:humidity_sensor_id>", methods=["GET"])
def get_humidity_sensor(humidity_sensor_id):
    result = HumiditySensor.query.get(humidity_sensor_id)
    status_code = 200 if result else 404
    response = result.to_dict() if result else {"error":"Not found"}
    return jsonify(response), status_code

@bp.route("/humidity-sensor", methods=["POST"])
def create_humidity_sensor():
    data = request.json
    new_data = HumiditySensor(
        name=data["name"],
        humidity=data["humidity"]
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify(new_data.to_dict()), 201
