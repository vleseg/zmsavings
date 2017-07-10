# Third-party imports
import attr
# Project imports
from datasource import CSVSource
import settings


# TODO: refactor
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


@attr.s
class Transaction(object):
    source = CSVSource(settings.TRANSACTIONS_CONN_SETTINGS)

    date = attr.ib()
    outcome_account_name = attr.ib()
    income_account_name = attr.ib()
    outcome = attr.ib()
    income = attr.ib()

    @classmethod
    def all(cls):
        for entry in cls.source.all():
            yield Transaction(
                date=entry['date'],
                outcome_account_name=entry['outcomeAccountName'],
                income_account_name=entry['incomeAccountName'],
                outcome=entry['outcome'],
                income=entry['income']
            )
