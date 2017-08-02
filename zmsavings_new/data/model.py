# Third-party imports
import attr
# Project imports
from connector import GoalConnector


class BaseModel(object):
    _connector = None

    @classmethod
    def select(cls, func):
        return filter(func, cls.all())

    @classmethod
    def all(cls):
        return (cls(**fields) for fields in cls._connector.all())


@attr.s
class Account(BaseModel):
    name = attr.ib()


@attr.s
class Goal(BaseModel):
    _connector = GoalConnector()

    # Fields
    account_name = attr.ib()
    start_date = attr.ib()


class ProgressiveTotal(BaseModel):
    pass


@attr.s
class Transaction(BaseModel):
    income_account = attr.ib()
    outcome_account = attr.ib()
    date = attr.ib()
