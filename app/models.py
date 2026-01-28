from sqlalchemy.sql import func
from .db import db


class Plant(db.Model):
    __tablename__ = "plants"

    __table_args__ = (
        db.UniqueConstraint("name", name="uq_plants_name"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    sensor = db.relationship(
        "Sensor",
        back_populates="plant",
        cascade="all, delete-orphan"
    )

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
class Sensor(db.Model):
    __tablename__ = "sensors"

    __table_args__ = (
        db.UniqueConstraint("pin", name="uq_sensors_pin"),
        db.UniqueConstraint("plant_id", name="uq_sensors_plant_id"),
        db.ForeignKeyConstraint(
            ["plant_id"],
            ["plants.id"],
            name="fk_readings_plant_id"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.String(10), nullable=False)
    plant_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime, 
        server_default=func.now()
    )
    updated_at = db.Column(
        db.DateTime, 
        server_default=func.now(), 
        onupdate=func.now()
    )

    plant = db.relationship("Plant", back_populates="sensor")
    readings = db.relationship(
        "HumidityReading",
        back_populates="sensor",
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

    __table_args__ = (
        db.ForeignKeyConstraint(
            ["sensor_id"],
            ["sensors.id"],
            name="fk_readings_sensor_id"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )

    sensor = db.relationship("Sensor", back_populates="readings")

    @classmethod
    def get_plants_readings(cls):
        subquery = (
            db.session.query(
                HumidityReading.sensor_id,
                func.max(HumidityReading.created_at).label("last_reading")
            )
            .group_by(HumidityReading.sensor_id)
            .subquery()
        )

        query = (
            db.session.query(
                Plant,
                HumidityReading.humidity,
                HumidityReading.created_at
            )
            .outerjoin(Sensor, Sensor.plant_id == Plant.id)
            .outerjoin(
                subquery,
                subquery.c.sensor_id == Sensor.id
            )
            .outerjoin(
                HumidityReading,
                (HumidityReading.sensor_id == Sensor.id) &
                (HumidityReading.created_at == subquery.c.last_reading)
            )
        )

        return query