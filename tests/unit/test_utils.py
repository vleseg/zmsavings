# Third-party imports
from mock import mock_open, patch
import pytest
# Project imports
from zmsavings_new.utils import (
    get_or_create_user_data_dir, read_path, read_yes_no,
    path_from_appdata_or_input)


class StopExecution(BaseException):
    pass


class TestPathFromAppdataOrInput(object):
    def setup(self):
        patcher = patch('zmsavings_new.utils.open', mock_open(), create=True)
        self._mock_open = patcher.start()
        self._mock_open.return_value.read.return_value = 'path_from_ptr_file'

        # Other mocks
        self._mock_os = patch('zmsavings_new.utils.os', spec_set=True).start()
        self._mock_os.path.isfile.return_value = True
        self._mock_read_yes_no = patch(
            'zmsavings_new.utils.read_yes_no').start()
        self._mock_get_or_create_udd = patch(
            'zmsavings_new.utils.get_or_create_user_data_dir').start()
        self._mock_get_or_create_udd.return_value = 'user_data_dir'
        self._mock_read_path = patch('zmsavings_new.utils.read_path').start()
        self._mock_read_path.return_value = 'new_path_to_csv'

    def test_gets_path_to_ptr_file_by_name_and_opens_it(self):
        path_from_appdata_or_input('something')

        self._mock_get_or_create_udd.assert_called_once()
        self._mock_os.path.join.assert_called_once_with(
            'user_data_dir', 'something')
        self._mock_open.assert_called_once_with(
            self._mock_os.path.join.return_value, 'r')

    def test_read_path_to_csv_file_from_ptr_file_and_return_it(self):
        self._mock_read_yes_no.return_value = True
        result = path_from_appdata_or_input('something')

        assert result == 'path_from_ptr_file'

    def test_asks_if_you_want_to_use_path_from_ptr(self):
        path_from_appdata_or_input('something')

        self._mock_read_yes_no.assert_called_once_with(
            "Do you want to use file 'path_from_ptr_file'?")

    def test_if_user_doesnt_want_to_use_path_from_ptr_prompts_another(self):
        self._mock_read_yes_no.return_value = False
        path_from_appdata_or_input('something')

        self._mock_read_path.assert_called_once_with(
            "Enter valid path to 'something'")

    def test_prompts_path_to_csv_file_if_pointer_file_nonexistent_returns_it(
            self):
        self._mock_os.path.isfile.return_value = False
        result = path_from_appdata_or_input('something')

        self._mock_read_path.assert_called_once_with(
            "Enter valid path to 'something'")
        assert result == self._mock_read_path.return_value

    @patch('zmsavings_new.utils.print_function')
    def test_prompts_path_to_csv_file_if_path_in_pointer_file_is_wrong(
            self, mock_print):
        # First call checks for ptr file, second call checks for csv file
        self._mock_os.path.isfile.side_effect = [True, False]
        path_from_appdata_or_input('something')

        mock_print.assert_called_once_with(
            "Stored path 'path_from_ptr_file' does not exist")
        self._mock_read_path.assert_called_with(
            "Enter valid path to 'something'")

    def test_creates_pointer_file_if_did_not_exist(self):
        path_to_ptr_file = self._mock_os.path.join.return_value
        self._mock_os.path.isfile.return_value = False
        path_from_appdata_or_input('something')

        self._mock_open.assert_called_once_with(path_to_ptr_file, 'w')

    def test_saves_correct_path_to_pointer_file(self):
        self._mock_os.path.isfile.return_value = False
        path_from_appdata_or_input('something')

        self._mock_open.return_value.write.assert_called_once_with(
            'new_path_to_csv')


@patch('zmsavings_new.utils.os', spec_set=True)
@patch('zmsavings_new.utils.appdirs', spec_set=True)
class TestGetUserDataDir(object):
    def test_gets_user_data_dir_from_appdirs_with_app_name(self,
                                                           mock_appdirs, _):
        result = get_or_create_user_data_dir()
        mock_appdirs.user_data_dir.assert_called_once_with('ZmSavings')

        assert result == mock_appdirs.user_data_dir.return_value

    def test_if_user_data_dir_does_not_exist_creates_it(self,
                                                        mock_appdirs, mock_os):
        mock_os.path.isdir.return_value = False
        result = get_or_create_user_data_dir()
        mock_appdirs_rv = mock_appdirs.user_data_dir.return_value

        mock_os.makedirs.assert_called_once_with(mock_appdirs_rv)
        assert result == mock_appdirs_rv


@patch('zmsavings_new.utils.print_function')
@patch('zmsavings_new.utils.os', spec_set=True)
@patch('zmsavings_new.utils.raw_input')
class TestReadPath(object):
    def test_adds_exit_instruction_to_prompt_and_reads_path_from_user(
            self, mock_raw_input, _, _2):
        result = read_path('enter path')

        mock_raw_input.assert_called_with('enter path (Ctrl+C to abort) ')
        assert result == mock_raw_input.return_value

    def test_if_entered_path_does_not_exist_prompts_again(
            self, mock_raw_input, mock_os, mock_print):
        mock_os.path.isfile.return_value = False
        # Must raise, because the function keeps asking for correct input
        # indefinitely
        mock_raw_input.side_effect = [0, 1, StopExecution]
        with pytest.raises(StopExecution):
            read_path('enter path')

        mock_print.assert_called_with('File does not exist')
        mock_raw_input.assert_called_with('enter path (Ctrl+C to abort) ')


@patch('zmsavings_new.utils.raw_input')
class TestReadYesNo(object):
    def test_adds_instruction_to_prompt_and_reads_from_user(self,
                                                            mock_raw_input):
        # Must raise, because the function keeps asking for correct input
        # indefinitely
        mock_raw_input.side_effect = StopExecution
        with pytest.raises(StopExecution):
            read_yes_no('confirm something')

        mock_raw_input.assert_called_with(
            'confirm something (y/n or Ctrl+C to abort) ')

    def test_y_return_true_n_return_false(self, mock_raw_input):
        mock_raw_input.side_effect = ['y', 'Y', 'n', 'N']

        assert read_yes_no('answer with y') is True
        assert read_yes_no('answer with Y') is True
        assert read_yes_no('answer with n') is False
        assert read_yes_no('answer with N') is False

    def test_prompts_again_on_other_answers(self, mock_raw_input):
        mock_raw_input.side_effect = [
            'yes', '123', 'please stop', '...', StopExecution]
        with pytest.raises(StopExecution):
            read_yes_no('no correct input')
