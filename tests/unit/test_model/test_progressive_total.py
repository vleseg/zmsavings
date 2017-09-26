from datetime import datetime
# Third-party imports
import pytest
from money import Money
# Project imports
from zmsavings_new.data.model import Goal, ProgressiveTotal, Transaction


def rur(value):
    return Money(value, 'RUR')


@pytest.fixture
def goal():
    return Goal(account='goal account', name='my goal',
                start_date=datetime(2014, 1, 1), total=rur(7000))


@pytest.fixture
def prog_total(goal):
    return ProgressiveTotal(goal, transactions=[])


def test_progressive_total_points_initialized_by_list_by_default(prog_total):
    assert prog_total.progressive_total_points == []


def test_calculates_progressive_total_based_on_transactions_given(prog_total):
    transactions = [
        Transaction(
            date=datetime(2015, 1, 1), income_account='goal account',
            outcome_account='other account', income=rur(100),
            outcome=rur(99)),
        Transaction(
            date=datetime(2015, 1, 2), income_account='goal account',
            outcome_account='', income=rur(25), outcome=rur(0)),
        Transaction(
            date=datetime(2015, 1, 3), income_account='',
            outcome_account='goal account', income=rur(0), outcome=rur(15)),
        Transaction(
            date=datetime(2015, 1, 4), income_account='other account',
            outcome_account='goal account', income=rur(0),
            outcome=rur('10.55')),
        Transaction(
            date=datetime(2015, 1, 5), income_account='',
            outcome_account='goal account', income=rur(0),
            outcome=rur(1)),
        Transaction(
            date=datetime(2015, 1, 6), income_account='goal account',
            outcome_account='other account 2', income=rur(1000),
            outcome=rur(1000)),
    ]
    prog_total.transactions = transactions
    prog_total.calculate()

    assert [p.total for p in prog_total.progressive_total_points] == [
        rur(100), rur(125), rur(110), rur('99.45'), rur('98.45'),
        rur('1098.45')
    ]
    assert [p.date for p in prog_total.progressive_total_points] == [
        datetime(2015, 1, 1), datetime(2015, 1, 2), datetime(2015, 1, 3),
        datetime(2015, 1, 4), datetime(2015, 1, 5), datetime(2015, 1, 6)
    ]


def test_is_income_transaction_returns_true_for_transfer_to_goal_acc(
        prog_total):
    transaction = Transaction(
        date=datetime(2015, 1, 1), income_account='goal account',
        outcome_account='other account', income=rur(100), outcome=rur(100))

    assert prog_total._is_income_transaction(transaction)


def test_is_income_transaction_returns_false_for_reverse_transfer(prog_total):
    transaction = Transaction(
        date=datetime(2015, 1, 1), income_account='other account',
        outcome_account='goal account', income=rur(100), outcome=rur(100))

    assert not prog_total._is_income_transaction(transaction)


def test_is_income_transaction_returns_false_for_pure_outcome(prog_total):
    transaction = Transaction(
        date=datetime(2015, 1, 1), income_account='',
        outcome_account='goal account', income=rur(0), outcome=rur(100))

    assert not prog_total._is_income_transaction(transaction)
