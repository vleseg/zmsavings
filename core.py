# Project imports
from data.aggregate import GoalTransactions
from data.model import Goal, Transaction
from visualization import visualize


def main():
    account_name_to_gt = {
        goal.account_name: GoalTransactions(goal) for goal in Goal.all()}
    for t in Transaction.all():
        try:
            acc_name = (set(account_name_to_gt.keys()) &
                        {t.income_account_name, t.outcome_account_name}).pop()
        # If money did not arrive or leave account, this transaction should be
        # skipped
        except KeyError:
            continue
        goal_transactions = account_name_to_gt[acc_name]
        if t.date >= goal_transactions.goal.start_date:
            goal_transactions.transactions.append(t)

    all_goal_transactions = account_name_to_gt.values()

    for gt in all_goal_transactions:
        gt.calculate_progressive_total()
        gt.fill_in_blanks()
        visualize(gt)


if __name__ == '__main__':
    main()
