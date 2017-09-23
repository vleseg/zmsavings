import types
from datetime import datetime
# Third-party imports
from mock import patch
# Project imports
from zmsavings_new.data.connector import GoalConnector
from zmsavings_new.data.model import Goal

patch.object = patch.object


class TestGoal(object):
    def setup(self):
        self._mock_all = patch.object(Goal._connector, 'all').start()
        self._mock_all.return_value = [
            {'account': 'foo', 'name': 'bar', 'total': 1000,
             'start_date': datetime(2010, 1, 1)},
            {'account': 'biz', 'name': 'baz', 'total': 2000,
             'start_date': datetime(2010, 2, 2)},
            {'account': 'abc', 'name': 'xyz', 'total': 3000,
             'start_date': datetime(2010, 3, 3)}
        ]

    @patch.object(Goal, 'all')
    def test_select_uses_callable_to_filter_all(self, mock_all):
        mock_all.return_value = ['apple', 'apricot', 'banana', 'aardvark']
        result = Goal.select(lambda s: s.startswith('a'))

        assert list(result) == ['apple', 'apricot', 'aardvark']

    def test_connector_initialized_on_class_declared(self):
        assert isinstance(Goal._connector, GoalConnector)

    def test_all_calls_all_of_underlying_connector(self):
        Goal.all()

        assert self._mock_all.called

    def test_all_returns_generator(self):
        result = Goal.all()

        assert isinstance(result, types.GeneratorType)

    def test_all_initializes_instances_with_data_from_connector(self):
        goals = list(Goal.all())

        assert [g.name for g in goals] == ['bar', 'baz', 'xyz']
        assert [g.start_date for g in goals] == [
            datetime(2010, 1, 1), datetime(2010, 2, 2), datetime(2010, 3, 3)
        ]
        assert [g.total for g in goals] == [1000, 2000, 3000]

    def test_init_creates_account_instance_for_passed_name(self):
        goals = list(Goal.all())

        assert [g.account.name for g in goals] == ['foo', 'biz', 'abc']
