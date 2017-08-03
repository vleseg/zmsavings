from importlib import import_module
# Third-party imports
from mock import Mock, patch
# Project imports
from zmsavings_new.data.connector import CsvConnector, GoalConnector


@patch('zmsavings_new.data.connector.path_from_appdata_or_input')
class TestGoalConnector(object):
    def test_goal_connector_is_a_csv_connector(self, _):
        assert isinstance(GoalConnector(), CsvConnector)

    def test_source_prop_calls_utility_method_with_filename_on_1st_invocation(
            self, m_utility):
        gc = GoalConnector()
        gc._source
        m_utility.assert_called_once_with('pathToGoalsCsv')

    def test_source_prop_returns_reader_prop_on_successive_invocations(self, _):
        gc = GoalConnector()
        gc._source
        assert gc._source == gc._reader

    @patch('zmsavings_new.data.connector.csv.reader')
    def test_reader_is_initialized_with_fp_returned_by_utility_method(
            self, m_reader, m_utility):
        gc = GoalConnector()
        gc._source
        gc._source
        m_reader.assert_called_once_with(m_utility.return_value)
        assert gc._reader == m_reader.return_value
