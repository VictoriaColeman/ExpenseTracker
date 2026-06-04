
class ExpenseGroup:
    def __init__(self, name):
        self.name = name
        self.members = []

    def __str__(self):
        memberNames = [user.name for user in self.members]
        return f"Group: {self.name}, Members: {", ".join(memberNames)}"

class Expense:
    def __init__(self, date, name, amount, payer, participants):
        self.date = date
        self.name = name
        self.amount = amount
        self.payer = payer
        self.participants = participants
        self.status = "unpaid"
        self.payments = []

class Debt:
    def __init__(self, creditor, debtor, amount):
        self.creditor = creditor
        self.debtor = debtor
        self.amount = amount

class Payment:
    def __init__(self, date, payer, payee, amount):
        self.date = date
        self.payer = payer
        self.payee = payee
        self.amount = amount

class User:
    def __init__(self, name):
        self.name = name
        self.debts = []
        self.owedAmounts = []

    def __str__(self):
        return f"{self.name}"

