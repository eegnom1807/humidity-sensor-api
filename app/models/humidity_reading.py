from sqlalchemy.sql import func
from ..models import Plant, Sensor
from ..db import db


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