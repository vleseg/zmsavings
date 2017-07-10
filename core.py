from model import Goal, Transaction


def main():
    goals = list(Goal.all())
    transactions = list(Transaction.all())


if __name__ == '__main__':
    main()
