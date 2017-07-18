from datetime import timedelta
# Third-party imports
import attr
from money import Money
# Project imports
from utils import pairwise


@attr.s
class ProgressiveTotalPoint(object):
    total = attr.ib()
    date = attr.ib()


@attr.s
class GoalTransactions(object):
    goal = attr.ib()
    transactions = attr.ib(default=attr.Factory(list))
    progressive_total = attr.ib(default=attr.Factory(list))

    def calculate_progressive_total(self):
        total = Money(0, 'RUR')

        for t in self.transactions:
            # In one transaction there is always either a meaningful income or
            # outcome. The other value is always zero.
            if t.income == Money(0, 'RUR'):
                total -= t.outcome
            else:
                total += t.income

            self.progressive_total.append(ProgressiveTotalPoint(total, t.date))

    def fill_in_blanks(self):
        without_blanks = []
        one_day = timedelta(days=1)

        for current, next_ in pairwise(self.progressive_total):
            without_blanks.append(current)
            if next_ is None:
                break
            filler_date = current.date + one_day
            while next_.date - filler_date >= one_day:
                without_blanks.append(ProgressiveTotalPoint(
                    total=current.total, date=filler_date))
                filler_date += one_day

        self.progressive_total = without_blanks
