# Third-party imports
import attr


@attr.s
class CsvConnectionSettings(object):
    path = attr.ib()
    use_fields = attr.ib()
    header_row = attr.ib(default=1)
