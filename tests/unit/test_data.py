from mock import patch
from zmsavings_new.data.model import BaseModel


class TestBase(object):
    @patch.object(BaseModel, 'all')
    def test_select_uses_predicate_to_filter_all(self, m_all):
        m_all.return_value = ['apple', 'apricot', 'banana', 'aardvark']
        result = BaseModel.select(lambda s: s.startswith('a'))
        assert list(result) == ['apple', 'apricot', 'aardvark']
