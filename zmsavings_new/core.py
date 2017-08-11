from data.model import Account, Goal, ProgressiveTotal, Transaction


def _select_transactions_for_goal(goal):
    account = Account.select(lambda a: a.name == goal.account.name)[0]
    return Transaction.select(
        lambda t:
            (t.income_account == account or t.outcome_account == account) and
            t.date >= goal.start_date)


def main():
    progressive_totals = []
    for g in Goal.all():
        transactions = _select_transactions_for_goal(g)
        progressive_totals.append(ProgressiveTotal(g, transactions))

    for pt in progressive_totals:
        pt.calculate()
        pt.visualize()


if __name__ == '__main__':
    main()
