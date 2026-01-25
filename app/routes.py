from flask import Blueprint, jsonify, request
from .models import Plant
from .db import db

bp = Blueprint("api", __name__)


@bp.route("/plants", methods=["GET"])
def get_all_plants():
    plants = []
    data = Plant.get_all()

    for row in data:
        plants.append({
            'id': row.id,
            'name': row.name,
            'species': row.species
        })

    return jsonify(plants), 200

@bp.route("/plants", methods=["POST"])
def add_plant():
    data = request.json
    plant = Plant(
        name=data["name"],
        species=data["species"]
    )

    try:
        db.session.add(plant)
        db.session.commit()
    except:
        error = {"message": "Conflict"}
        return error, 409
    
    message = {"message": "Created"}
    return jsonify(message), 201

@bp.route("/plants/<int:id>", methods=["GET"])
def get_plant_by_id(id):
    data = Plant.get_by_id(id)
    if data is None:
        error = {"message":  "Not Found"}
        return error, 404
    
    plant = {
        "id": data.id,
        "name": data.name,
        "species": data.species
    }

    return jsonify(plant), 200

@bp.route("/plants/<int:id>", methods=["PUT"])
def update_plant(id):
    plant = Plant.get_by_id(id)
    if plant is None:
        error = {"message":  "Not Found"}
        return error, 404
    
    new_data = request.json
    plant.name = new_data["name"]
    plant.species = new_data["species"]

    try:
        db.session.commit()
    except:
        error = {"message":  "Conflict"}
        return error, 409
    
    return {}, 204

@bp.route("/plants/<int:id>", methods=["DELETE"])
def delete_plant(id):
    plant = Plant.get_by_id(id)
    if plant is None:
        error = {"message":  "Not Found"}
        return error, 404

    try:
        db.session.delete(plant)
        db.session.commit()
    except:
        error = {"message":  "Conflict"}
        return error, 409
    
    return {}, 200
        
