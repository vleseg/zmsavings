# Third-party imports
import unicodecsv as csv
# Project imports
from utils.fs import path_from_appdata_or_input
from utils.converter import Converter


class AdHocConnector(object):
    def __init__(self, unique=False):
        self._unique = unique
        self._container = []

    def all(self):
        return iter(self._container)

    def store(self, item):
        if self._unique and item in self._container:
            return
        self._container.append(item)


class CsvConnector(object):
    _csv2model_fields = {}
    _header_line_no = 1
    _pointer_filename = ''
    _use_all_csv_fields = True

    def __init__(self):
        self._data = None

    @property
    def _source(self):
        if self._data is None:
            path_to_csv = path_from_appdata_or_input(self._pointer_filename)
            with open(path_to_csv, 'rb') as f:
                self._data = list(csv.reader(f))
        return self._data

    def _get_model_field_to_idx_mapping(self):
        result = {}
        csv_header_line = self._source[self._header_line_no-1]
        for i, field_header in enumerate(csv_header_line):
            if field_header in self._csv2model_fields:
                result[self._csv2model_fields[field_header]] = i
            elif self._use_all_csv_fields:  # +same field name in csv and model
                result[field_header] = i

        return result

    def all(self):
        model_field2row_idx = self._get_model_field_to_idx_mapping()

        for row in self._source[self._header_line_no:]:
            row_dict = {}
            for model_field, idx in model_field2row_idx.items():
                if isinstance(model_field, Converter):
                    value = model_field(row[idx])
                    model_field = model_field.model_field_name
                else:
                    value = row[idx]
                row_dict[model_field] = value

            yield row_dict


class GoalConnector(CsvConnector):
    _csv2model_fields = dict(
        accountName='account',
        goalName='name',
        startDate=Converter.to_datetime('start_date', fmt='%d.%m.%Y'),
        total=Converter.to_rubles('total')
    )
    _pointer_filename = 'pathToGoalsCsv'


class TransactionConnector(CsvConnector):
    _csv2model_fields = dict(
        date=Converter.to_datetime('date', fmt='%Y-%m-%d'),
        outcomeAccountName='outcome_account',
        outcome=Converter.to_rubles('outcome'),
        incomeAccountName='income_account',
        income=Converter.to_rubles('income'),
    )
    _header_line_no = 4
    _pointer_filename = 'pathToTransactionsCsv'
    _use_all_csv_fields = False
