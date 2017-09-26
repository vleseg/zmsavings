from datetime import datetime
# Third-party imports
from money import Money
# Project imports
from zmsavings_new.data.model import ProgressiveTotal, Transaction


def rur(value):
    return Money(value, 'RUR')


class TestProgressiveTotal(object):
    def test_progressive_total_points_initialized_by_list_by_default(self):
        pt = ProgressiveTotal('goal name', transactions=[])

        assert pt.progressive_total_points == []

    def test_calculates_progressive_total_based_on_transactions_given(self):
        transactions = [
            Transaction(
                date=datetime(2015, 1, 1), income_account='goal_account',
                outcome_account='other_account', income=rur(100),
                outcome=rur(99)),
            Transaction(
                date=datetime(2015, 1, 2), income_account='goal_account',
                outcome_account='', income=rur(25), outcome=rur(0)),
            Transaction(
                date=datetime(2015, 1, 3), income_account='',
                outcome_account='goal_account', income=rur(0), outcome=rur(15)),
            Transaction(
                date=datetime(2015, 1, 4), income_account='other_account',
                outcome_account='goal_account', income=rur(0),
                outcome=rur('10.55')),
            Transaction(
                date=datetime(2015, 1, 5), income_account='goal_account',
                outcome_account='other_account_2', income=rur(1000),
                outcome=rur(1000)),
        ]
        pt = ProgressiveTotal('my goal', transactions=transactions)
        pt.calculate()

        assert [p.total for p in pt.progressive_total_points] == [
            rur(100), rur(125), rur(110), rur('99.45'), rur('1099.45')
        ]
        assert [p.date for p in pt.progressive_total_points] == [
            datetime(2015, 1, 1), datetime(2015, 1, 2), datetime(2015, 1, 3),
            datetime(2015, 1, 4), datetime(2015, 1, 5)
        ]
