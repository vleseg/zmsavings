# Third-party imports
from mock import patch
# Project imports
from zmsavings_new.data.connector import CsvConnector, GoalConnector
from zmsavings_new.meta.settings import CsvConnectionSettings


class TestGoalConnector(object):
    def test_goal_connector_is_a_csv_connector(self):
        assert isinstance(GoalConnector(), CsvConnector)

    @patch('zmsavings_new.data.connector.CsvConnectionSettings')
    def test_uses_corresponding_settings_to_connect_to_csv_source(self,
                                                                  m_settings):
        assert isinstance(GoalConnector._settings_map, dict)
        c = GoalConnector()
        m_settings.assert_called_once_with(**c._settings_map)
