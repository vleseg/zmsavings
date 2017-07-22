# Project imports
from meta.settings import CsvConnectionSettings
from utils import path_from_appdata_or_input


APP_NAME = 'zmsavings'
GOAL_CONN_SETTINGS = CsvConnectionSettings(
    path=path_from_appdata_or_input('goalsFile', 'CSV with goals'),
)
TRANSACTIONS_CONN_SETTINGS = CsvConnectionSettings(
    path=path_from_appdata_or_input(
        'transactionsFile', 'CSV with transactions'),
    use_fields=[
        'date', 'outcomeAccountName', 'outcome', 'incomeAccountName', 'income'],
    header_row=4
)
