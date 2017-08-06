# Third-party imports
import unicodecsv as csv
# Project imports
from utils import path_from_appdata_or_input


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
        headers = self._source[0]
        return (dict(zip(headers, row)) for row in self._source[1:])


class GoalConnector(CsvConnector):
    _pointer_filename = 'pathToGoalsCsv'
