
class ExpenseGroup:
    def __init__(self, name, groupsList, userList):
        self.name = name
        self.members = []
        self.addGroupMembers(userList)
        if not self.members:
            print("You did not add any group members. The expense group was not created.")
        else:
            groupsList.append(self)
            print("The following expense group was created:")
            print("  " + str(self))

    def __str__(self):
        memberNames = [user.name for user in self.members]
        return f"Group: {self.name}, Members: {", ".join(memberNames)}"

    def addGroupMembers(self, userList):
        newMembers = input("Please enter group members, separated by commas: ")
        parsedNames = [name.strip() for name in newMembers.split(',')]
        currentMemberNames = [member.name for member in self.members]
        newMemberNames = []
        duplicates = []
        newUserNames = []
        for name in parsedNames:
            if name:
                if name not in currentMemberNames and name not in newMemberNames:
                    newMemberNames.append(name)
                else:
                    duplicates.append(name)
        if duplicates:
            print("The following users are already in this group and will not be added:")
            for duplicate in duplicates:
                print(f"  {duplicate}")
        for name in newMemberNames:
            existingUser = False
            for user in userList:
                if user.name == name:
                    self.members.append(user)
                    existingUser = True
            if not existingUser:
                newUser = User(name, userList)
                self.members.append(newUser)
                newUserNames.append(name)
        if newUserNames:
            print("The following users were not yet in the system and were added:")
            for name in newUserNames:
                print(f"  {name}")

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
    def __init__(self, name, userList):
        self.name = name
        self.debts = []
        self.owedAmounts = []
        userList.append(self)

    def __str__(self):
        return f"{self.name}"

