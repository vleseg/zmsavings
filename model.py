# Third-party imports
import attr
# Project imports
from datasource import CSVSource
import settings


@attr.s
class Goal(object):
    source = CSVSource(settings.GOAL_CONN_SETTINGS)

    name = attr.ib()
    account_name = attr.ib()
    total = attr.ib()

    @classmethod
    def all(cls):
        for entry in cls.source.all():
            yield Goal(
                name=entry['goalName'],
                account_name=entry['accountName'],
                total=entry['total']
            )
