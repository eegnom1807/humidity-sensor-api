from flask import Blueprint, jsonify, request
from .models import HumiditySensor
from .extensions import db

bp = Blueprint("api", __name__, url_prefix="/api/v1")


@bp.route("/humidity-sensor", methods=["GET"])
def get_all_humidity_sensor():
    data = HumiditySensor.query.all()
    return jsonify(data), 200

@bp.route("/humidity-sensor/<int:humidity_sensor_id>", methods=["GET"])
def get_humidity_sensor(humidity_sensor_id):
    data = HumiditySensor.query.get(humidity_sensor_id)
    return jsonify(data) if data else {"error":"Not found"}

# POST
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
