# Third-party imports
from mock import mock_open, patch
# Project imports
from zmsavings_new.data.connector import CsvConnector, GoalConnector


class TestGoalConnector(object):
    def setup(self):
        patcher = patch(
            'zmsavings_new.data.connector.open', mock_open(), create=True)
        self._mock_open = patcher.start()

        # Other mocks
        self._mock_get_path = patch(
            'zmsavings_new.data.connector.path_from_appdata_or_input').start()
        self._mock_get_path.return_value = 'path_to_csv_file'
        self._mock_reader = patch(
            'zmsavings_new.data.connector.csv.reader', spec_set=True).start()
        self._mock_reader.return_value = iter(['csv\n', 'file\n', 'content\n'])

    def test_goal_connector_is_a_csv_connector(self):
        assert isinstance(GoalConnector(), CsvConnector)

    def test_getting_source_prop_1st_time_calls_utility_method(self):
        gc = GoalConnector()
        _ = gc._source

        self._mock_get_path.assert_called_once_with('pathToGoalsCsv')

    def test_getting_source_prop_1st_time_reads_source_csv_and_stores_content(
            self):
        gc = GoalConnector()
        _ = gc._source

        self._mock_open.assert_called_once_with('path_to_csv_file', 'rb')
        assert gc._data == ['csv\n', 'file\n', 'content\n']

    def test_getting_source_prop_2nd_time_returns_data_prop(self):
        gc = GoalConnector()
        _ = gc._source

        assert gc._source == gc._data

    @patch('zmsavings_new.data.connector.iter')
    def test_all_returns_iterator_over_source(self, mock_iter):
        with patch.object(GoalConnector, '_source') as mock_source:
            GoalConnector().all()
            mock_iter.assert_called_once_with(mock_source)
