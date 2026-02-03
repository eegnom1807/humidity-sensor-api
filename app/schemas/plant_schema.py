from ..extensions import ma
from marshmallow import fields, validate


class PlantSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100)
    )
    image_url = fields.Str(
        required=True,
        validate=validate.Length(min=0, max=255)
    )
    active = fields.Bool(required=False)

plant_schema = PlantSchema()
plants_schema = PlantSchema(many=True)