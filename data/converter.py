from datetime import datetime


class Converter(object):
    @classmethod
    def to_datetime(cls, field_name, fmt):
        return cls(field_name, convert=lambda s: datetime.strptime(s, fmt))

    def __init__(self, field_name, convert):
        self.field_name = field_name
        self.convert = convert
