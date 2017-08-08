from datetime import date
# Third-party imports
from mock import Mock, patch
import pytest
# Project imports
from zmsavings_new.core import (
    _select_transactions_for_goal, Account, Goal, Transaction)


@pytest.fixture()
def accounts():
    patcher = patch.object(Account, 'all')
    m_all = patcher.start()
    correct_account = Account(name='correct')
    incorrect_account = Account(name='incorrect')
    m_all.return_value = [correct_account, incorrect_account]

    return correct_account, incorrect_account


@pytest.fixture()
def correct_transactions(accounts):
    correct_account, incorrect_account = accounts
    patcher = patch.object(Transaction, 'all')
    m_all = patcher.start()
    correct_transactions = [
        Transaction(income_account=correct_account,
                    outcome_account=incorrect_account, date=date(2017, 3, 3)),
        Transaction(income_account=incorrect_account,
                    outcome_account=correct_account, date=date(2017, 3, 3))
    ]
    m_all.return_value = [
        Transaction(income_account=incorrect_account,
                    outcome_account=incorrect_account, date=date(2017, 3, 3)),
        correct_transactions[0],
        Transaction(income_account=correct_account,
                    outcome_account=incorrect_account, date=date(2017, 1, 1)),
        correct_transactions[1]
    ]

    return correct_transactions


def test_select_transactions_by_account_and_date(correct_transactions):
    goal = Goal(name='my goal', account_name='correct', total=1000,
                start_date=date(2017, 2, 2))
    result = _select_transactions_for_goal(goal)
    assert result == correct_transactions
