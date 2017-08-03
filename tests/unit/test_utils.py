import os
# Third-party imports
from mock import mock_open, patch
# Project imports
from zmsavings_new.utils import path_from_appdata_or_input


class TestPathFromAppdataOrInput(object):
    def setup(self):
        patcher = patch('zmsavings_new.utils.open', mock_open(), create=True)
        self._mock_open = patcher.start()

    @patch('zmsavings_new.utils.get_user_data_dir')
    def test_gets_path_to_ptr_file_by_name_and_opens_it(self, m_get_dir):
        m_get_dir.return_value = 'bogus_parent'
        path_from_appdata_or_input('bogus')
        m_get_dir.assert_called_once()
        self._mock_open.assert_called_once_with(
            os.path.join('bogus_parent', 'bogus'), 'rb')

    @patch('zmsavings_new.utils.get_user_data_dir')
    def test_returns_opened_file(self, m_get_dir):
        m_get_dir.return_value = 'something'
        result = path_from_appdata_or_input('something else')
        assert result == self._mock_open.return_value

    def test_prompts_path_to_csv_file_if_pointer_file_nonexistent(self):
        pass

    def test_prompts_path_to_csv_file_if_path_in_pointer_file_is_wrong(self):
        pass

    def test_creates_pointer_file_if_did_not_exist(self):
        pass

    def test_saves_correct_path_to_pointer_file(self):
        pass
