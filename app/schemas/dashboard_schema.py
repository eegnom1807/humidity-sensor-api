from ..extensions import ma
from marshmallow import fields
from ..utils import get_date


class DashboardSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    image_url = fields.Str()
    active = fields.Bool()
    humidity = fields.Float()
    last_reading = fields.Method("format_created")

    def format_created(self, obj):
        return get_date(obj["last_reading"]) if obj["last_reading"] != None else ""

dashoboard_schema = DashboardSchema(many=True)