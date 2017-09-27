from datetime import datetime
# Project imports
from zmsavings_new.utils.misc import get_today


def test_get_today_returns_today_as_datetime_without_time():
    today_without_time = datetime(
        datetime.today().year, datetime.today().month, datetime.today().day)

    assert get_today() == today_without_time
