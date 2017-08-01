from mock import patch
from zmsavings_new.data.model import BaseModel, Goal
from zmsavings_new.data.connector import GoalConnector


class TestBase(object):
    @patch.object(BaseModel, 'all')
    def test_select_uses_callable_to_filter_all(self, m_all):
        m_all.return_value = ['apple', 'apricot', 'banana', 'aardvark']
        result = BaseModel.select(lambda s: s.startswith('a'))
        assert list(result) == ['apple', 'apricot', 'aardvark']


class TestGoal(object):
    def test_connector_initialized_on_class_declared(self):
        assert isinstance(Goal._connector, GoalConnector)

    @patch.object(Goal._connector, 'all')
    def test_all_calls_all_of_underlying_connector(self, m_all):
        Goal.all()
        assert m_all.called
