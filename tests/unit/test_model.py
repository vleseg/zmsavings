from datetime import datetime
import types
# Third-party imports
from mock import patch
import pytest
# Project imports
from zmsavings_new.data.model import Account, AdHocModel, BaseModel, Goal
from zmsavings_new.data.connector import GoalConnector


class TestBase(object):
    @patch.object(BaseModel, 'all')
    def test_select_uses_callable_to_filter_all(self, m_all):
        m_all.return_value = ['apple', 'apricot', 'banana', 'aardvark']
        result = BaseModel.select(lambda s: s.startswith('a'))

        assert list(result) == ['apple', 'apricot', 'aardvark']


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

        assert [g.account for g in goals] == [
            Account(name='foo'), Account(name='biz'), Account(name='abc')
        ]


class TestAccount(object):
    def test_is_an_ad_hoc_model(self):
        a = Account('my account')

        assert isinstance(a, AdHocModel)

    def test_cannot_be_initialized_without_name(self):
        with pytest.raises(TypeError):
            Account()
        a = Account('my account')

        assert a.name == 'my account'

    @patch.object(Account, '_connector')
    def test_stores_new_instance_to_ad_hoc_connector(self, mock_connector):
        a = Account('my account')

        mock_connector.store.assert_called_once_with(a)

    @patch.object(Account, '_connector')
    def test_all_returns_all_previously_stored_models(self, mock_connector):
        mock_container = []
        mock_connector.store = lambda item: mock_container.append(item)
        mock_connector.all.return_value = mock_container

        Account('my account')
        Account('your account')
        Account('our account')

        assert [a.name for a in Account.all()] == [
            'my account', 'your account', 'our account'
        ]
