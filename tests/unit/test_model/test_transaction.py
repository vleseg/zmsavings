from datetime import datetime
# Third-party imports
from mock import patch
# Project imports
from data.model import Transaction

patch.object = patch.object


class TestTransaction(object):
    def setup(self):
        self._mock_all = patch.object(Transaction._connector, 'all').start()
        self._mock_all.return_value = [
            {'income_account': 'foo', 'outcome_account': 'bar', 'income': 1000,
             'outcome': 1000, 'date': datetime(2010, 1, 1)},
            {'income_account': 'bar', 'outcome_account': 'foo', 'income': 2000,
             'outcome': 2100, 'date': datetime(2010, 2, 2)},
            {'income_account': 'bar', 'outcome_account': '', 'income': 3000,
             'outcome': 0, 'date': datetime(2010, 3, 3)}
        ]

    def test_all_initializes_instances_with_data_from_connector(self):
        transactions = list(Transaction.all())

        assert [t.income_account for t in transactions] == ['foo', 'bar', 'bar']
        assert [t.outcome_account for t in transactions] == ['bar', 'foo', '']
        assert [t.income for t in transactions] == [1000, 2000, 3000]
        assert [t.outcome for t in transactions] == [1000, 2100, 0]
        assert [t.date for t in transactions] == [
            datetime(2010, 1, 1), datetime(2010, 2, 2), datetime(2010, 3, 3)
        ]
