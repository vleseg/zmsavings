from datetime import datetime
import types
# Third-party imports
from mock import patch
# Project imports
from zmsavings_new.data.model import BaseModel, Goal
from zmsavings_new.data.connector import GoalConnector


class TestBase(object):
    @patch.object(BaseModel, 'all')
    def test_select_uses_callable_to_filter_all(self, m_all):
        m_all.return_value = ['apple', 'apricot', 'banana', 'aardvark']
        result = BaseModel.select(lambda s: s.startswith('a'))
        assert list(result) == ['apple', 'apricot', 'aardvark']


@patch.object(Goal._connector, 'all')
class TestGoal(object):
    def test_connector_initialized_on_class_declared(self, _):
        assert isinstance(Goal._connector, GoalConnector)

    def test_all_calls_all_of_underlying_connector(self, m_all):
        Goal.all()
        assert m_all.called

    def test_returns_generator(self, _):
        result = Goal.all()
        assert isinstance(result, types.GeneratorType)

    def test_returns_instance_parametrized_by_value_from_connector(self, m_all):
        m_all.return_value = [
            {'account_name': 'foo', 'start_date': datetime(2010, 1, 1)},
            {'account_name': 'bar', 'start_date': datetime(2010, 2, 2)},
            {'account_name': 'abc', 'start_date': datetime(2010, 3, 3)}
        ]
        assert list(Goal.all()) == [
            Goal(account_name='foo', start_date=datetime(2010, 1, 1)),
            Goal(account_name='bar', start_date=datetime(2010, 2, 2)),
            Goal(account_name='abc', start_date=datetime(2010, 3, 3))
        ]
