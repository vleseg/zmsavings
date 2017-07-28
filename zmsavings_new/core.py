from zmsavings_new.data.model import (
    Account, Goal, ProgressiveTotal, Transaction)


def _select_transactions_for_goal(goal):
    account = Account.select(lambda a: a.name == goal.account_name)
    return Transaction.select(
        lambda t: (t.income_account == account or t.outcome_account == account)
                  and t.date >= goal.start_date)


def main():
    progressive_totals = []
    for g in Goal.all():
        progressive_totals.append(ProgressiveTotal(g))
        transactions = _select_transactions_for_goal(g)
