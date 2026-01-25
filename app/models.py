from sqlalchemy.sql import func
from .db import db


class Plant(db.Model):
    __tablename__ = "plants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    species = db.Column(db.String(100), nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    humidity_readings = db.relationship(
        "HumidityReading",
        back_populates="plant",
        cascade="all, delete-orphan"
    )

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

class HumidityReading(db.Model):
    __tablename__ = "humidity_readings"

    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(
        db.Integer,
        db.ForeignKey("plants.id"),
        nullable=False
    )
    humidity = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(100), nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )

    # reverse relation
    plant = db.relationship("Plant", back_populates="humidity_readings")