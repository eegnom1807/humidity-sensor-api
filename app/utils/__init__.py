import os
from flask import request, abort
from datetime import timezone, timedelta

GMT_6 = timezone(timedelta(hours=-6))


def get_date(date):
    return str(date.replace(tzinfo=timezone.utc).astimezone(GMT_6))

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
