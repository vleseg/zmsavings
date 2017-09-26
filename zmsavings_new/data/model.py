# Third-party imports
import attr
from money import Money
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

    def _is_income_transaction(self, transaction):
        if transaction.income == Money(0, 'RUR'):
            return False
        if transaction.income_account != self.goal.account:
            return False
        return True

    def calculate(self):
        current_total = Money(0, 'RUR')

        for t in self.transactions:
            if self._is_income_transaction(t):
                current_total += t.income
            else:
                current_total -= t.outcome
            self.progressive_total_points.append(
                ProgressiveTotalPoint(total=Money(current_total.amount, 'RUR'),
                                      date=t.date))


@attr.s
class ProgressiveTotalPoint(BaseModel):
    total = attr.ib()
    date = attr.ib()


@attr.s
class Transaction(BaseModel):
    _connector = TransactionConnector()

    date = attr.ib()
    income_account = attr.ib(convert=Account.factory)
    outcome_account = attr.ib(convert=Account.factory)
    income = attr.ib()
    outcome = attr.ib()
