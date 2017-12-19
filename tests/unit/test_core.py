# Third-party imports
from mock import call, Mock, patch
# Project imports
from zmsavings.core import _select_transactions_for_goal, main


@patch('core.ProgressiveTotal')
@patch('core._select_transactions_for_goal')
class TestMain(object):
    def setup_method(self):
        self._goal_patcher = patch('core.Goal')
        self._m_goal = self._goal_patcher.start()
        self._m_goal.all = Mock(return_value=['goal_1', 'goal_2', 'goal_3'])

    def test_calls_select_transactions_for_each_goal(self, mock_select, _):
        main()
        assert mock_select.mock_calls == [
            call('goal_1'), call('goal_2'), call('goal_3')]

    def test_gets_all_goals(self, _, _2):
        main()
        assert self._m_goal.all.called

    def test_inits_progressive_totals_with_goals_and_transactions(
            self, mock_select, mock_pt):
        self._m_goal.all = Mock(return_value=['goal_1', 'goal_2', 'goal_3'])
        mock_select.side_effect = [
            ['tr_1_1', 'tr_1_2', 'tr_1_3'],
            ['tr_2_1', 'tr_2_2', 'tr_2_3'],
            ['tr_3_1', 'tr_3_2', 'tr_3_3']
        ]
        main()
        assert mock_pt.call_args_list == [
            call('goal_1', ['tr_1_1', 'tr_1_2', 'tr_1_3']),
            call('goal_2', ['tr_2_1', 'tr_2_2', 'tr_2_3']),
            call('goal_3', ['tr_3_1', 'tr_3_2', 'tr_3_3'])
        ]

    def test_calculate_called_for_each_progressive_total(self, _, mock_pt):
        mock_pt_objects = [Mock()] * 3
        mock_pt.side_effect = mock_pt_objects
        main()
        assert all(
            mock_pt_obj.calculate.called for mock_pt_obj in mock_pt_objects)

    def test_visualize_called_for_each_progressive_total(self, _, mock_pt):
        mock_pt_instances = [Mock()] * 3
        mock_pt.side_effect = mock_pt_instances
        main()
        assert all(
            mock_pt_obj.visualize.called for mock_pt_obj in mock_pt_instances)

    def teardown_method(self):
        self._goal_patcher.stop()


@patch('core.Account', spec_set=True)
@patch('core.Transaction', spec_set=True)
class TestSelectTransactions(object):
    def test_selects_acc_and_then_its_transactions_by_cryptic_callables(
            self, mock_transaction, mock_account):
        mock_account.select = Mock(return_value=['account'])
        mock_transaction.select = Mock(return_value=['tr_1', 'tr_2', 'tr_3'])

        result = _select_transactions_for_goal('goal')
        assert mock_account.select.called
        assert callable(mock_account.select.call_args[0][0])
        assert mock_transaction.select.called
        assert callable(mock_transaction.select.call_args[0][0])
        assert result == ['tr_1', 'tr_2', 'tr_3']
