from datetime import datetime
# Third-party imports
from mock import mock_open, patch
from money import Money
import pytest
# Project imports
from zmsavings_new.data.connector import (
    AdHocConnector, CsvConnector, GoalConnector, TransactionConnector)


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

    def test_converts_field_names_from_csv_to_field_names_of_model(self,
                                                                   mocks):
        mocks.reader.return_value = [
            ['accountName', 'goalName', 'total', 'startDate'],
            ['foo', 'bar', '1000', '01.01.2016']
        ]
        gc = GoalConnector()

        actual_dict_keys = sorted(list(gc.all())[0].keys())
        assert actual_dict_keys == sorted(
            ['account', 'name', 'start_date', 'total']
        )

    def test_converts_date_field_into_datetime_object(self, mocks):
        mocks.reader.return_value = [
            ['accountName', 'goalName', 'total', 'startDate'],
            ['foo', 'bar', '1000', '04.05.2016']
        ]
        gc = GoalConnector()
        gc_entry = list(gc.all())[0]

        assert gc_entry['start_date'] == datetime(2016, 5, 4)

    def test_converts_amount_field_into_money_object(self, mocks):
        mocks.reader.return_value = [
            ['accountName', 'goalName', 'total', 'startDate'],
            ['biz', 'baz', '5000,50', '06.06.2017']
        ]
        gc = GoalConnector()
        gc_entry = list(gc.all())[0]

        assert gc_entry['total'] == Money('5000.50', 'RUR')


class TestAdHocConnector(object):
    def test_store_stores_item_in_the_inner_container(self):
        ahc = AdHocConnector()
        ahc.store('something')
        ahc.store('something else')

        assert ahc._container == ['something', 'something else']

    def test_all_returns_iterator_over_items_in_container(self):
        ahc = AdHocConnector()
        ahc.store('one')
        ahc.store('two')
        ahc.store('three')

        assert list(ahc.all()) == ['one', 'two', 'three']

    def test_if_initialized_as_unique_does_not_store_duplicate_values(self):
        ahc = AdHocConnector(unique=True)
        ahc.store("unique")
        ahc.store('duplicate')
        ahc.store('another unique')
        ahc.store('duplicate')

        stored = list(ahc.all())
        assert len(stored) == 3
        assert stored.count('duplicate') == 1


class TestTransactionConnector(object):
    def test_use_only_declared_csv_fields(self, mocks):
        tc = TransactionConnector()
        tc._header_line_no = 1
        mocks.reader.return_value = [
            ['date', 'do not use me', 'outcomeAccountName', 'pls no', 'outcome',
             'incomeAccountName', 'ha ha', 'no no no', 'income'],
            ['2017-11-30', 'aaa', 'bbb', 'ccc', '100', 'ddd', 'eee', 'iii',
             '200'],
        ]
        res_keys, res_values = zip(*next(tc.all()).items())

        assert sorted(res_keys) == sorted(
            ['date', 'outcome_account', 'outcome', 'income_account', 'income'])
        assert set(res_values) == {datetime(2017, 11, 30), Money(200, 'RUR'),
                                   Money(100, 'RUR'), 'bbb', 'ddd'}

    def test_starts_reading_file_from_specified_header_line(self, mocks):
        tc = TransactionConnector()
        tc._header_line_no = 5
        mocks.reader.return_value = [
            ['skip me'], ['skip', 'me too'], ['...'], ['start', 'with', 'next'],
            ['outcomeAccountName', 'outcome', 'incomeAccountName', 'income',
             'date', 'excess field'],
            ['aaa', '15', 'bbb', '25', '2016-12-31', 'ccc'],
        ]
        res_keys, res_values = zip(*next(tc.all()).items())

        assert sorted(res_keys) == sorted(
            ['date', 'outcome_account', 'outcome', 'income_account', 'income'])
        assert set(res_values) == {datetime(2016, 12, 31), Money(15, 'RUR'),
                                   Money(25, 'RUR'), 'aaa', 'bbb'}
