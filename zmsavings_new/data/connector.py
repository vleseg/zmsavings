# Project imports
from zmsavings_new.meta.settings import CsvConnectionSettings


class CsvConnector(object):
    _settings_map = {}

    def __init__(self):
        self._settings = CsvConnectionSettings(**self._settings_map)


class GoalConnector(CsvConnector):
    def all(self):
        pass
