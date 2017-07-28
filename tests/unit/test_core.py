# Third-party imports
from mock import call, Mock, patch
# Project imports
from zmsavings_new import core
from zmsavings_new.data.model import Account, Goal, Transaction


@patch('zmsavings_new.core.Goal')
@patch('zmsavings_new.core.ProgressiveTotal')
@patch('zmsavings_new.core._select_transactions_for_goal')
class TestMain(object):
    def test_gets_all_goals_and_inits_progressive_totals_with_them(
            self, _, m_pt, m_goal):
        m_goal.all = Mock(return_value=['goal_1', 'goal_2', 'goal_3'])
        core.main()
        assert m_goal.all.called
        assert m_pt.mock_calls == [
            call('goal_1'), call('goal_2'), call('goal_3')]

    def test_calls_select_transactions_for_each_goal(self, m_select, _, m_goal):
        m_goal.all = Mock(return_value=['goal_1', 'goal_2', 'goal_3'])
        core.main()
        assert m_select.mock_calls == [
            call('goal_1'), call('goal_2'), call('goal_3')]


@patch('zmsavings_new.core.Account', spec_set=Account)
@patch('zmsavings_new.core.Transaction', spec_set=Transaction)
class TestSelectTransactions(object):
    def test_selects_acc_and_then_its_transactions_by_cryptic_callables(
            self, m_tr, m_account):
        m_account.select = Mock()
        m_tr.select = Mock(return_value=['tr_1', 'tr_2', 'tr_3'])

        result = core._select_transactions_for_goal('goal')
        assert m_account.select.called
        assert callable(m_account.select.call_args[0][0])
        assert m_tr.select.called
        assert callable(m_tr.select.call_args[0][0])
        assert result == ['tr_1', 'tr_2', 'tr_3']
