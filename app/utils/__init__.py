import os
from flask import request, abort
from datetime import timezone, timedelta


def get_date(date):
    time_zone = timezone(timedelta(hours=-6))
    new_date = date.replace(tzinfo=timezone.utc).astimezone(time_zone)

    return new_date.strftime("%Y-%m-%d %H:%M:%S")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
    
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def require_api_key():
    api_key = request.headers.get("X-API-KEY")
    if not api_key or api_key != os.getenv("API_KEY"):
        abort(401, description="Invalid API key")
