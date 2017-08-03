# Third-party imports
import unicodecsv as csv
# Project imports
from zmsavings_new.utils import path_from_appdata_or_input


class CsvConnector(object):
    pass


class GoalConnector(CsvConnector):
    _pointer_filename = 'pathToGoalsCsv'

    def __init__(self):
        self._reader = None

    @property
    def _source(self):
        if self._reader is None:
            self._reader = csv.reader(
                path_from_appdata_or_input(self._pointer_filename))
        return self._reader

    def all(self):
        pass
