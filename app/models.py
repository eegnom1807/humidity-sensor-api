# humidity_sensor = [
#     {"id": 1, "name": "Plant 1", "humidity": "223", "created_at": "2018-01-01 00:00:00" },
#     {"id": 2, "name": "Plant 2", "humidity": "323", "created_at": "2018-02-01 00:00:00" },
# ]

from datetime import datetime
from .extensions import db


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