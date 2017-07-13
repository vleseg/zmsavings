# Project imports
import settings
from data.datasource import CsvSource


class CsvConnector(object):
    connection_settings = None
    model2csv_fields = {}

    def __init__(self):
        self.source = CsvSource(self.connection_settings)

    def all(self):
        for entry in self.source.all():
            yield {
                model_field: entry[csv_field] for model_field, csv_field
                in self.model2csv_fields.items()}


class GoalConnector(CsvConnector):
    connection_settings = settings.GOAL_CONN_SETTINGS
    model2csv_fields = dict(
        name='goalName',
        account_name='accountName',
        total='total',
    )


class TransactionConnector(CsvConnector):
    connection_settings = settings.TRANSACTIONS_CONN_SETTINGS
    model2csv_fields = dict(
        date='date',
        outcome_account_name='outcomeAccountName',
        income_account_name='incomeAccountName',
        outcome='outcome',
        income='income',
    )