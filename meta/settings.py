# Third-party imports
import attr
# Project imports
import validators


@attr.s
class CSVConnectionSettings(object):
    path = attr.ib(validator=validators.file_exists)
    use_fields = attr.ib()
    header_row = attr.ib(default=1)
