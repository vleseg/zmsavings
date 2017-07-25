# Third-party imports
import attr
# Project imports
from constants import ALL


@attr.s
class CsvConnectionSettings(object):
    path = attr.ib()
    use_fields = attr.ib(default=ALL)
    header_row = attr.ib(default=1)
