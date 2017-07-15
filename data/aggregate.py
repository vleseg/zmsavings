# Third-party imports
import attr


@attr.s
class GoalTransactions(object):
    goal = attr.ib()
    transactions = attr.ib(default=attr.Factory(list))
