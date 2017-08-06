# Third-party imports
from mock import mock_open, patch
import pytest
# Project imports
from zmsavings_new.data.connector import CsvConnector, GoalConnector


@pytest.fixture
def mocks():
    class Mocks(object):
        pass

    fixture_obj = Mocks()
    fixture_obj.open = patch(
        'zmsavings_new.data.connector.open', mock_open(), create=True).start()
    fixture_obj.get_path = patch(
        'zmsavings_new.data.connector.path_from_appdata_or_input').start()
    fixture_obj.get_path.return_value = 'path_to_csv_file'
    fixture_obj.reader = patch(
        'zmsavings_new.data.connector.csv.reader', spec_set=True).start()
    fixture_obj.reader.return_value = iter(['csv\n', 'file\n', 'content\n'])

    return fixture_obj


@pytest.mark.userfixtures('mocks')
class TestGoalConnector(object):
    def test_goal_connector_is_a_csv_connector(self):
        assert isinstance(GoalConnector(), CsvConnector)

    def test_getting_source_prop_1st_time_calls_utility_method(self, mocks):
        gc = GoalConnector()
        _ = gc._source

        mocks.get_path.assert_called_once_with('pathToGoalsCsv')

    def test_getting_source_prop_1st_time_reads_source_csv_and_stores_content(
            self, mocks):
        gc = GoalConnector()
        _ = gc._source

        mocks.open.assert_called_once_with('path_to_csv_file', 'rb')
        assert gc._data == ['csv\n', 'file\n', 'content\n']

    def test_getting_source_prop_2nd_time_returns_data_prop(self):
        gc = GoalConnector()
        _ = gc._source

        assert gc._source == gc._data


@pytest.mark.userfixtures('mocks')
class TestGoalConnectorAll(object):
    def test_all_returns_iterable_of_dicts_formed_from_read_csv_data(self,
                                                                     mocks):
        mocks.reader.return_value = [
            ['ship_name', 'ship_class', 'tiryampampation_type'],
            ['Blackbird 9000', 'striker', 'null-t'],
            ['Lux Aeterna', 'wanderer', 'warp']
        ]
        gc = GoalConnector()
        result = list(gc.all())

        assert result == [
            {'ship_name': 'Blackbird 9000', 'ship_class': 'striker',
             'tiryampampation_type': 'null-t'},
            {'ship_name': 'Lux Aeterna', 'ship_class': 'wanderer',
             'tiryampampation_type': 'warp'}
        ]
