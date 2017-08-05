# Third-party imports
import unicodecsv as csv
# Project imports
from zmsavings_new.utils import path_from_appdata_or_input


class CsvConnector(object):
    _pointer_filename = ''

    def __init__(self):
        self._data = None

    @property
    def _source(self):
        if self._data is None:
            path_to_csv = path_from_appdata_or_input(self._pointer_filename)
            with open(path_to_csv, 'rb') as f:
                self._data = list(csv.reader(f))
        return self._data

    def all(self):
        return iter(self._source)


class GoalConnector(CsvConnector):
    _pointer_filename = 'pathToGoalsCsv'
