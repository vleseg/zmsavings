from datetime import datetime
# Third-party imports
from money import Money


class Converter(object):
    def __init__(self, model_field_name, convert_method):
        self.model_field_name = model_field_name
        self._convert = convert_method

    def __call__(self, value):
        return self._convert(value)

    @classmethod
    def to_datetime(cls, model_field_name, fmt):
        def _convert(value):
            return datetime.strptime(value, fmt)

        return cls(model_field_name, _convert)

    @classmethod
    def to_rubles(cls, model_field_name):
        def _convert(value):
            return Money(amount=value.replace(',', '.'), currency='RUR')

        return cls(model_field_name, _convert)
