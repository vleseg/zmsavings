# Third-party imports
import attr
# Project imports
from connector import AdHocConnector, GoalConnector, TransactionConnector


class BaseModel(object):
    _connector = None

    @classmethod
    def select(cls, func):
        return filter(func, cls.all())

    @classmethod
    def all(cls):
        return (cls(**fields) for fields in cls._connector.all())


class AdHocModel(BaseModel):
    _connector = AdHocConnector()

    def __attrs_post_init__(self):
        self._connector.store(self)

    @classmethod
    def all(cls):
        return cls._connector.all()


@attr.s
class Account(AdHocModel):
    name = attr.ib()


@attr.s
class Goal(BaseModel):
    _connector = GoalConnector()

    # Fields
    account = attr.ib(convert=Account)
    name = attr.ib()
    start_date = attr.ib()
    total = attr.ib()


class ProgressiveTotal(BaseModel):
    pass


@attr.s
class Transaction(BaseModel):
    _connector = TransactionConnector()

    date = attr.ib()
    income_account = attr.ib()
    outcome_account = attr.ib()
    income = attr.ib()
    outcome = attr.ib()
