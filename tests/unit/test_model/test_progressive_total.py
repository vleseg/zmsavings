from datetime import datetime
# Third-party imports
import pytest
from mock import patch
from money import Money
# Project imports
from zmsavings_new.data.model import Goal, ProgressiveTotal, Transaction


def rur(value):
    return Money(value, 'RUR')


@pytest.fixture
def fixture():
    class Fixture(object):
        pass

    fixture_obj = Fixture()
    fixture_obj.goal = Goal(account='goal account', name='my goal',
                            start_date=datetime(2014, 1, 1), total=rur(7000))
    fixture_obj.prog_total = ProgressiveTotal(fixture_obj.goal, transactions=[
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
    ])

    fixture_obj.mock_get_today = patch(
        'zmsavings_new.data.model.get_today').start()
    fixture_obj.mock_get_today.return_value = datetime(2015, 1, 6)

    return fixture_obj


def test_progressive_total_points_initialized_by_list_by_default(fixture):
    assert fixture.prog_total.progressive_total_points == []


def test_calculate_handles_empty_transaction_list_correctly(fixture):
    fixture.prog_total.transactions = []
    fixture.prog_total.calculate()

    assert fixture.prog_total.progressive_total_points == []


def test_calculates_progressive_total_based_on_transactions_given(fixture):
    fixture.prog_total.calculate()

    assert [p.total for p in fixture.prog_total.progressive_total_points] == [
        rur(100), rur(125), rur(110), rur('99.45'), rur('98.45'),
        rur('1098.45')
    ]
    assert [p.date for p in fixture.prog_total.progressive_total_points] == [
        datetime(2015, 1, 1), datetime(2015, 1, 2), datetime(2015, 1, 3),
        datetime(2015, 1, 4), datetime(2015, 1, 5), datetime(2015, 1, 6)
    ]


def test_calculate_fills_in_missed_dates_between_transaction(fixture):
    fixture.prog_total.transactions.insert(0, Transaction(
        datetime(2014, 12, 28), income_account='goal account',
        outcome_account='other account', income=rur(50), outcome=rur('48.50')
    ))
    fixture.prog_total.transactions.extend([
        Transaction(
            datetime(2015, 1, 9), income_account='goal account',
            outcome_account='', income=rur('99.99'), outcome=rur(0)),
        Transaction(
            datetime(2015, 1, 11), income_account='other account 2',
            outcome_account='goal_account', income=rur(150), outcome=rur(150))
    ])
    fixture.mock_get_today.return_value = datetime(2015, 1, 11)
    fixture.prog_total.calculate()

    assert [p.total for p in fixture.prog_total.progressive_total_points] == [
        rur(50), rur(50), rur(50), rur(50), rur(150), rur(175), rur(160),
        rur('149.45'), rur('148.45'), rur("1148.45"), rur("1148.45"),
        rur("1148.45"), rur('1248.44'), rur('1248.44'), rur('1098.44')
    ]
    assert [p.date for p in fixture.prog_total.progressive_total_points] == [
        datetime(2014, 12, 28), datetime(2014, 12, 29), datetime(2014, 12, 30),
        datetime(2014, 12, 31), datetime(2015, 1, 1), datetime(2015, 1, 2),
        datetime(2015, 1, 3), datetime(2015, 1, 4), datetime(2015, 1, 5),
        datetime(2015, 1, 6), datetime(2015, 1, 7), datetime(2015, 1, 8),
        datetime(2015, 1, 9), datetime(2015, 1, 10), datetime(2015, 1, 11),
    ]


def test_calculate_fills_in_dates_up_until_today(fixture):
    fixture.mock_get_today.return_value = datetime(2015, 1, 10)
    fixture.prog_total.calculate()
    last_ptp = fixture.prog_total.progressive_total_points[-1]

    assert len(fixture.prog_total.progressive_total_points) == 10
    assert last_ptp.date == datetime(2015, 1, 10)


def test_is_income_transaction_returns_true_for_transfer_to_goal_acc(fixture):
    transaction = Transaction(
        date=datetime(2015, 1, 1), income_account='goal account',
        outcome_account='other account', income=rur(100), outcome=rur(100))

    assert fixture.prog_total._is_income_transaction(transaction)


def test_is_income_transaction_returns_false_for_reverse_transfer(fixture):
    transaction = Transaction(
        date=datetime(2015, 1, 1), income_account='other account',
        outcome_account='goal account', income=rur(100), outcome=rur(100))

    assert not fixture.prog_total._is_income_transaction(transaction)


def test_is_income_transaction_returns_false_for_pure_outcome(fixture):
    transaction = Transaction(
        date=datetime(2015, 1, 1), income_account='',
        outcome_account='goal account', income=rur(0), outcome=rur(100))

    assert not fixture.prog_total._is_income_transaction(transaction)
