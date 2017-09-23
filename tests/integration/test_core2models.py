from datetime import date
# Third-party imports
from mock import patch
import pytest
# Project imports
from zmsavings_new.core import (
    _select_transactions_for_goal, Account, Goal, Transaction)

patch.object = patch.object


@pytest.fixture()
def accounts():
    patcher = patch.object(Account, 'all')
    mock_all = patcher.start()
    patch.object(Account, '_connector').start()

    correct_account = Account(name='correct')
    incorrect_account = Account(name='incorrect')
    mock_all.return_value = [correct_account, incorrect_account]

    yield correct_account, incorrect_account
    patcher.stop()


@pytest.fixture()
def correct_transactions(accounts):
    correct_account, incorrect_account = accounts
    patcher = patch.object(Transaction, 'all')
    mock_all = patcher.start()
    correct_transactions = [
        Transaction(income_account=correct_account, income=1000, outcome=0,
                    outcome_account=incorrect_account, date=date(2017, 3, 3)),
        Transaction(income_account=incorrect_account, income=2000, outcome=0,
                    outcome_account=correct_account, date=date(2017, 3, 3))
    ]
    mock_all.return_value = [
        Transaction(income_account=incorrect_account, income=0, outcome=111,
                    outcome_account=incorrect_account, date=date(2017, 3, 3)),
        correct_transactions[0],
        Transaction(income_account=correct_account, income=0, outcome=222,
                    outcome_account=incorrect_account, date=date(2017, 1, 1)),
        correct_transactions[1]
    ]

    return correct_transactions


def test_select_transactions_by_account_and_date(correct_transactions):
    goal = Goal(name='my goal', account='correct', total=1000,
                start_date=date(2017, 2, 2))
    result = _select_transactions_for_goal(goal)
    assert result == correct_transactions
