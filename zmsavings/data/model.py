# Third-party imports
import attr
# Project imports
from connector import GoalConnector, TransactionConnector


class BaseModel(object):
    connector = None

    @classmethod
    def all(cls):
        for init_kwargs in cls.connector.all():
            yield cls(**init_kwargs)


@attr.s
class Goal(BaseModel):
    connector = GoalConnector()

    name = attr.ib()
    account_name = attr.ib()
    total = attr.ib()
    start_date = attr.ib()


@attr.s
class Transaction(BaseModel):
    connector = TransactionConnector()

    date = attr.ib()
    outcome_account_name = attr.ib()
    income_account_name = attr.ib()
    outcome = attr.ib()
    income = attr.ib()
