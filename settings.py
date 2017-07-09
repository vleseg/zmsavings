# Project imports
from meta.settings import CSVConnectionSettings


GOAL_CONN_SETTINGS = CSVConnectionSettings(
    path=raw_input("Path to CSV with goals: "),
    use_fields=['goalName', 'accountName', 'total']
)
