# Third-party imports
from mock import call, Mock, patch
# Project imports
from zmsavings_new.core import _select_transactions_for_goal, main


@patch('zmsavings_new.core.ProgressiveTotal')
@patch('zmsavings_new.core._select_transactions_for_goal')
class TestMain(object):
    def setup_method(self):
        self._goal_patcher = patch('zmsavings_new.core.Goal')
        self._m_goal = self._goal_patcher.start()
        self._m_goal.all = Mock(return_value=['goal_1', 'goal_2', 'goal_3'])

    def test_calls_select_transactions_for_each_goal(self, m_select, _):
        main()
        assert m_select.mock_calls == [
            call('goal_1'), call('goal_2'), call('goal_3')]

    def test_gets_all_goals(self, _, _2):
        main()
        assert self._m_goal.all.called

    def test_inits_progressive_totals_with_goals_and_transactions(
            self, m_select, m_pt):
        self._m_goal.all = Mock(return_value=['goal_1', 'goal_2', 'goal_3'])
        m_select.side_effect = [
            ['tr_1_1', 'tr_1_2', 'tr_1_3'],
            ['tr_2_1', 'tr_2_2', 'tr_2_3'],
            ['tr_3_1', 'tr_3_2', 'tr_3_3']
        ]
        main()
        assert m_pt.call_args_list == [
            call('goal_1', ['tr_1_1', 'tr_1_2', 'tr_1_3']),
            call('goal_2', ['tr_2_1', 'tr_2_2', 'tr_2_3']),
            call('goal_3', ['tr_3_1', 'tr_3_2', 'tr_3_3'])
        ]

    def test_calculate_called_for_each_progressive_total(self, _, m_pt):
        m_pt_instances = [Mock()] * 3
        m_pt.side_effect = m_pt_instances
        main()
        assert all(m_pt_inst.calculate.called for m_pt_inst in m_pt_instances)

    def test_visualize_called_for_each_progressive_total(self, _, m_pt):
        m_pt_instances = [Mock()] * 3
        m_pt.side_effect = m_pt_instances
        main()
        assert all(m_pt_inst.visualize.called for m_pt_inst in m_pt_instances)

    def teardown_method(self):
        self._goal_patcher.stop()


@patch('zmsavings_new.core.Account', spec_set=True)
@patch('zmsavings_new.core.Transaction', spec_set=True)
class TestSelectTransactions(object):
    def test_selects_acc_and_then_its_transactions_by_cryptic_callables(
            self, m_tr, m_account):
        m_account.select = Mock(return_value=['account'])
        m_tr.select = Mock(return_value=['tr_1', 'tr_2', 'tr_3'])

        result = _select_transactions_for_goal('goal')
        assert m_account.select.called
        assert callable(m_account.select.call_args[0][0])
        assert m_tr.select.called
        assert callable(m_tr.select.call_args[0][0])
        assert result == ['tr_1', 'tr_2', 'tr_3']
