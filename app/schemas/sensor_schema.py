from app.extensions import ma
from marshmallow import fields, validate, validates, ValidationError
from app.models.plant import Plant


class SensorSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    pin = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=10)
    )
    plant_id = fields.Int(required=True)

    @validates("plant_id")
    def validate_plant_exists(self, value, **kwargs):
        if not Plant.query.get(value):
            raise ValidationError("Plant does not exist")

sensor_schema = SensorSchema()
sensors_schema = SensorSchema(many=True)