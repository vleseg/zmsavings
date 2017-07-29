import attr


class BaseModel(object):
    @classmethod
    def select(cls, func):
        return filter(func, cls.all())

    @staticmethod
    def all():
        pass


@attr.s
class Account(BaseModel):
    name = attr.ib()


@attr.s
class Goal(BaseModel):
    account_name = attr.ib()
    start_date = attr.ib()


class ProgressiveTotal(BaseModel):
    pass


@attr.s
class Transaction(BaseModel):
    income_account = attr.ib()
    outcome_account = attr.ib()
    date = attr.ib()
