from datetime import datetime
from decimal import Decimal
# Third-party imports
from money import Money
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

    def test_calling_to_datetime_converter_converts_string_to_datetime(self):
        converter = Converter.to_datetime('bogus', fmt='%Y-%m-%d %H:%M:%S')
        result = converter('2017-02-02 17:18:19')

        assert result == datetime(
            year=2017, month=2, day=2, hour=17, minute=18, second=19)

    def test_calling_to_rubles_converter_converts_strings_to_currency_obj(self):
        converter = Converter.to_rubles('some_cash')
        result = converter('123')

        assert isinstance(result, Money)
        assert int(result.amount) == 123
        assert result.currency == 'RUR'

    def test_to_rubles_handles_decimal_comma_correctly(self):
        converter = Converter.to_rubles('money')
        result = converter('3,62')

        assert result.amount == Decimal('3.62')

    def test_to_rubles_converts_empty_string_to_zero(self):
        converter = Converter.to_rubles('rubles')
        result = converter('')

        assert int(result.amount) == 0
