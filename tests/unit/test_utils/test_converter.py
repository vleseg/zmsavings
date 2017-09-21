from datetime import datetime
# Project imports
from utils.converter import Converter


class TestConverter(object):
    def test_to_datetime_returns_converter_instance(self):
        assert isinstance(
            Converter.to_datetime('start_date', fmt='%Y-%m-%d'), Converter)

    def test_to_datetime_initializes_converter_w_field_name_and_callable(self):
        converter = Converter.to_datetime('start_date', fmt='%d.%m.%Y')

        assert converter.model_field_name == 'start_date'
        assert callable(converter._convert)

    def test_calling_tp_datetime_converter_converts_string_to_datetime(self):
        converter = Converter.to_datetime('bogus', fmt='%Y-%m-%d %H:%M:%S')

        result = converter('2017-02-02 17:18:19')
        assert result == datetime(
            year=2017, month=2, day=2, hour=17, minute=18, second=19)
