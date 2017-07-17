# Project imports
import settings
from datasource import CsvSource
from converter import Converter


class CsvConnector(object):
    connection_settings = None
    model2csv_fields = {}

    def __init__(self):
        self.source = CsvSource(self.connection_settings)

    def all(self):
        for entry in self.source.all():
            result = {}

            for model_field, csv_field in self.model2csv_fields.items():
                if isinstance(csv_field, Converter):
                    value = csv_field.convert(entry[csv_field.field_name])
                else:
                    value = entry[csv_field]
                result[model_field] = value

            yield result


class GoalConnector(CsvConnector):
    connection_settings = settings.GOAL_CONN_SETTINGS
    model2csv_fields = dict(
        name='goalName',
        account_name='accountName',
        total=Converter.to_rubles('total'),
        start_date=Converter.to_datetime('startDate', fmt='%d.%m.%Y'),
    )


class TransactionConnector(CsvConnector):
    connection_settings = settings.TRANSACTIONS_CONN_SETTINGS
    model2csv_fields = dict(
        date=Converter.to_datetime('date', fmt="%Y-%m-%d"),
        outcome_account_name='outcomeAccountName',
        income_account_name='incomeAccountName',
        outcome=Converter.to_rubles('outcome'),
        income=Converter.to_rubles('income'),
    )
