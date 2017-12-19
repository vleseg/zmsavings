from datetime import datetime


def get_today():
    return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
