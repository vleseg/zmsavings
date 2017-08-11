# Third-party imports
import unicodecsv as csv
# Project imports
from utils import path_from_appdata_or_input


# TODO: make _container set; rename class accordingly
class AdHocConnector(object):
    def __init__(self):
        self._container = []

    def all(self):
        return iter(self._container)

    def store(self, item):
        self._container.append(item)


class CsvConnector(object):
    _pointer_filename = ''
    _csv2model_fields = {}

    def __init__(self):
        self._data = None

    @property
    def _source(self):
        if self._data is None:
            path_to_csv = path_from_appdata_or_input(self._pointer_filename)
            with open(path_to_csv, 'rb') as f:
                self._data = list(csv.reader(f))
        return self._data

    # TODO: extract getting headers
    def all(self):
        headers = [
            self._csv2model_fields.get(csv_field_header, csv_field_header)
            for csv_field_header in self._source[0]
        ]
        return (dict(zip(headers, row)) for row in self._source[1:])


class GoalConnector(CsvConnector):
    _pointer_filename = 'pathToGoalsCsv'
    _csv2model_fields = dict(
        accountName='account',
        goalName='name',
        startDate='start_date',
    )


class TransactionConnector(CsvConnector):
    pass
