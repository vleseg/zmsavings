# Third-party imports
from mock import Mock, patch, call
import pytest
# Project imports
from zmsavings_new import core


class TestMain(object):
    @patch.object(core, 'Goal')
    @patch.object(core, 'GoalTransaction')
    def test_gets_all_goals_and_inits_goal_transactions_from_them(
            self, m_gt, m_goal):
        m_goal.all = Mock(return_value=['goal_1', 'goal_2', 'goal_3'])
        core.main()
        assert m_goal.all.called
        assert m_gt.mock_calls == [
            call('goal_1'), call('goal_2'), call('goal_3')]
