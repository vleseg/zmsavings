# Third-party imports
import pytest
from mock import patch
# Project imports
from zmsavings_new.data.model import Account, AdHocModel

patch.object = patch.object


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

    def test_factory_returns_none_if_name_is_empty_string(self):
        assert Account.factory('') is None

    def test_if_account_object_is_passed_to_factory_this_obj_is_returned(self):
        a = Account('konto')

        assert Account.factory(a) is a
