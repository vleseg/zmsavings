# Project imports
from meta.settings import CSVConnectionSettings
from utils import path_from_appdata_or_input


APP_NAME = 'zmsavings'
GOAL_CONN_SETTINGS = CSVConnectionSettings(
    path=path_from_appdata_or_input(APP_NAME, 'goalsFile', 'CSV with goals'),
    use_fields=['goalName', 'accountName', 'total']
)
