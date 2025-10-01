from datetime import datetime
from .db import db


class HumiditySensor(db.Model):
    __tablename__ = "sensor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def to_dict(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "humidity": self.humidity,
            "created_at": self.created_at
        }