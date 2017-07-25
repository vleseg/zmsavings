from datetime import datetime
# Third-party imports
from money import Money


class Converter(object):
    @classmethod
    def to_datetime(cls, field_name, fmt):
        return cls(field_name, convert=lambda s: datetime.strptime(s, fmt))

    @classmethod
    def to_rubles(cls, field_name):
        def convert(s):
            if not s:
                s = '0'
            # TODO: Find "correct" way to read RU locale decimals
            return Money(amount=s.replace(',', '.'), currency='RUR')

        return cls(field_name, convert)

    def __init__(self, field_name, convert):
        self.field_name = field_name
        self.convert = convert
