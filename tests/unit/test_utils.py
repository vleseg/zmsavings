import os
# Third-party imports
from mock import mock_open, patch
# Project imports
from zmsavings_new.utils import get_user_data_dir, path_from_appdata_or_input


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


@patch('zmsavings_new.utils.os', spec_set=True)
@patch('zmsavings_new.utils.appdirs', spec_set=True)
class TestGetUserDataDir(object):
    def test_gets_user_data_dir_from_appdirs_with_app_name(self, m_appdirs, _):
        result = get_user_data_dir()
        m_appdirs.user_data_dir.assert_called_once_with('ZmSavings')

        assert result == m_appdirs.user_data_dir.return_value

    def test_if_user_data_dir_does_not_exist_creates_it(self, m_appdirs, m_os):
        m_os.path.isdir.return_value = False
        result = get_user_data_dir()
        m_appdirs_rv = m_appdirs.user_data_dir.return_value

        m_os.makedirs.assert_called_once_with(m_appdirs_rv)
        assert result == m_appdirs_rv
