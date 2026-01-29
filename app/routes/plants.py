from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from ..models import Plant
from ..utils import get_date, allowed_file
from ..db import db
import os

plants_bp = Blueprint("plants", __name__)


@plants_bp.route("/plants", methods=["GET"])
def get_all_plants():
    plants = []
    data = Plant.get_all()

    for row in data:
        plants.append({
            "id": row.id,
            "name": row.name,
            "image_url": row.image_url,
            "active": row.active,
            "created_at": get_date(row.created_at),
            "updated_at": get_date(row.updated_at)
        })

    return jsonify(plants), 200

@plants_bp.route("/plants", methods=["POST"])
def add_plant():
    data = request.json
    
    plant = Plant(
        name=data["name"],
        image_url=data["image_url"],
        active=data["active"]
    )

    try:
        db.session.add(plant)
        db.session.commit()
    except:
        db.session.rollback()
        error = {"message": "Conflict"}
        return error, 409
    
    message = {"message": "Created"}
    return jsonify(message), 201

@plants_bp.route("/plants/<int:id>", methods=["GET"])
def get_plant_by_id(id):
    data = Plant.get_by_id(id)
    if data is None:
        error = {"message":  "Not Found"}
        return error, 404
    
    plant = {
        "id": data.id,
        "name": data.name,
        "image_url": data.image_url,
        "active": data.active,
        "created_at": get_date(data.created_at),
        "updated_at": get_date(data.updated_at)
    }

    return jsonify(plant), 200

@plants_bp.route("/plants/<int:id>", methods=["PUT"])
def update_plant(id):
    plant = Plant.get_by_id(id)
    if plant is None:
        error = {"message":  "Not Found"}
        return error, 404
    
    new_data = request.json
    plant.name = new_data["name"]
    plant.image_url = new_data["image_url"]
    plant.active = new_data["active"]

    try:
        db.session.commit()
    except:
        db.session.rollback()
        error = {"message":  "Conflict"}
        return error, 409
    
    return {}, 204

@plants_bp.route("/plants/<int:id>", methods=["DELETE"])
def delete_plant(id):
    plant = Plant.get_by_id(id)
    if plant is None:
        error = {"message":  "Not Found"}
        return error, 404

    try:
        db.session.delete(plant)
        db.session.commit()
    except:
        db.session.rollback()
        error = {"message":  "Conflict"}
        return error, 409
    
    return {}, 200

@plants_bp.route("/plants/<int:id>/image", methods=["POST"])
def upload_image(id):
    plant = Plant.get_by_id(id)
    if plant is None:
        error = {"message":  "Not Found"}
        return error, 404

    if "image_url" not in request.files:
        error = {"message":  "photo file is required"}
        return error, 400

    file = request.files["image_url"]
    if file.filename == "":
        error = {"message":  "Empty filename"}
        return error, 400

    if not allowed_file(file.filename):
        error = {"message":  "invalid file type"}
        return error, 400

    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[1].lower()

    upload_dir = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        "plants"
    )

    os.makedirs(upload_dir, exist_ok=True)
    final_filename = f"{plant.id}.{ext}"
    file_path = os.path.join(upload_dir, final_filename)
    file.save(file_path)

    plant.image_url = f"/uploads/plants/{final_filename}"
    db.session.commit()

    return jsonify({
        "status": "ok",
        "image_url": plant.image_url
    })