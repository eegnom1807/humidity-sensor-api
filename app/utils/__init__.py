from datetime import timezone, timedelta

GMT_6 = timezone(timedelta(hours=-6))

def get_date(date):
    return str(date.replace(tzinfo=timezone.utc).astimezone(GMT_6))