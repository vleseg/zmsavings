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
    _connector = AdHocConnector(unique=True)

    def __attrs_post_init__(self):
        self._connector.store(self)

    @classmethod
    def all(cls):
        return cls._connector.all()


@attr.s
class Account(AdHocModel):
    name = attr.ib()

    @classmethod
    def factory(cls, account_name):
        if isinstance(account_name, cls):
            return account_name
        elif len(account_name) > 0:
            return cls(account_name)
        else:
            return None


@attr.s
class Goal(BaseModel):
    _connector = GoalConnector()

    # Fields
    account = attr.ib(convert=Account)
    name = attr.ib()
    start_date = attr.ib()
    total = attr.ib()


@attr.s
class ProgressiveTotal(BaseModel):
    goal = attr.ib()
    transactions = attr.ib()
    progressive_total_points = attr.ib(default=attr.Factory(list))


@attr.s
class Transaction(BaseModel):
    _connector = TransactionConnector()

    date = attr.ib()
    income_account = attr.ib(convert=Account.factory)
    outcome_account = attr.ib(convert=Account.factory)
    income = attr.ib()
    outcome = attr.ib()
