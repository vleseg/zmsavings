from zmsavings_new.data.model import Goal, GoalTransaction


def main():
    goal_transactions = []
    for g in Goal.all():
        goal_transactions.append(GoalTransaction(g))
