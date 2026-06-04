from main import getYesNoAnswer, getValidDate, getValidDollarAmt
from datetime import datetime

class ExpenseGroup:
    def __init__(self, name, groupsList, userList):
        self.name = name.lower()
        self.members = []
        self.expenses = []
        self.debts = []
        self.payments = []
        self.addGroupMembers(userList)
        if not self.members:
            print("You did not add any group members. The expense group was not created.")
        else:
            groupsList.append(self)
            print("The following expense group was created:")
            print("  " + str(self))

    def __str__(self):
        memberNames = [user.name.title() for user in self.members]
        return f"Group: {self.name.title()}, Members: {", ".join(memberNames)}"

    def addGroupMembers(self, userList):
        newMembers = input("Please enter group members, separated by commas: ")
        parsedNames = [name.strip().lower() for name in newMembers.split(',')]
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
                print(f"  {duplicate.title()}")
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
                print(f"  {name.title()}")

    def checkForExistingMember(self, name, userList):
        existingGroupMember = False
        existingUser = False
        for member in self.members:
            if member.name == name.lower():
                person = member
                existingGroupMember = True
        if not existingGroupMember:
            addMember = getYesNoAnswer(f"{name.title()} is not a member in this expense group. Would you like to add them? (Y/N): ")
            if not addMember:
                return False
            for user in userList:
                if user.name == name.lower():
                    self.members.append(user)
                    person = user
                    existingUser = True
            if not existingUser:
                person = User(name, userList)
                self.members.append(person)
        return person

    def getExistingMember(self, prompt):
        existingMember = False
        while not existingMember:
            user = input(prompt).lower()
            for member in self.members:
                if member.name == user:
                    existingMember = True
                    user = member
            if not existingMember:
                print("That is not an existing group member. Please choose an existing member.")
        return user

    def recordPayment(self):
        date = getValidDate("\nPayment date (MM/DD/YYYY): ")
        payer = self.getExistingMember("Who made the payment?: ")
        payee = self.getExistingMember("Who received the payment?: ")
        invalidTransaction = False
        if payer == payee:
            print("Invalid payment. Payer and recipient cannot be the same. Please try again.")
            invalidTransaction = True
        if not invalidTransaction:
            invalidTransaction = True
            for debt in self.debts:
                if debt.creditor == payee and debt.debtor == payer and debt.amount > 0:
                    invalidTransaction = False
        if invalidTransaction:
            print(f"Invalid payment. {payer} does not owe {payee} anything. Payment not recorded.")
        else:
            validAmount = False
            while not validAmount:
                payment = getValidDollarAmt("Payment amount: ")
                for debt in self.debts:
                    if debt.creditor == payee and debt.debtor == payer and payment <= debt.amount:
                        validAmount = True
                        debt.amount -= payment
                        if debt.amount == 0:
                            self.debts.remove(debt)
                if not validAmount:
                    print("That is not a valid amount. Amount paid cannot be greater than amount owed. Please try again.")
            newPayment = Payment(date, payer, payee, payment, self)
            print(f"The following payment was recorded:\n  {newPayment}")

class Expense:
    def __init__(self, date, name, amount, payer, expenseGroup, userList):
        self.date = date
        self.name = name
        self.amount = amount
        self.payer = payer
        self.participants = self.getParticipants(expenseGroup, userList)
        expenseGroup.expenses.append(self)
        self.createDebts(expenseGroup)

    def __str__(self):
        participants = [participant.name.title() for participant in self.participants]
        return f"{self.date}: {self.payer} paid ${self.amount} for {self.name}. Expense split by: {", ".join(participants)}"

    def getParticipants(self, expenseGroup, userList):
        response = input("Please enter all participants who should split the expense separated by commas (including payer if applicable): ")
        parsedNames = [name.strip().lower() for name in response.split(',')]
        participants = []
        for name in parsedNames:
            user = expenseGroup.checkForExistingMember(name, userList)
            if user and user not in participants:
                participants.append(user)
        return participants

    def createDebts(self, expenseGroup):
        share = self.amount/len(self.participants)
        share = round(share, 2)
        for participant in self.participants:
            if participant != self.payer:
                newBalance = True
                for debt in expenseGroup.debts:
                    if debt.creditor == self.payer and debt.debtor == participant:
                        debt.addDebt(share)
                        newBalance = False
                if newBalance:
                    Debt(self.payer, participant, share, expenseGroup)


class Debt:
    def __init__(self, creditor, debtor, amount, expenseGroup):
        self.creditor = creditor
        self.debtor = debtor
        self.amount = amount
        expenseGroup.debts.append(self)

    def __str__(self):
        return f"{self.debtor} owes {self.creditor} ${self.amount}."

    def addDebt(self, amount):
        if amount > 0:
            self.amount += amount

class Payment:
    def __init__(self, date, payer, payee, amount, expenseGroup):
        self.date = date
        self.payer = payer
        self.payee = payee
        self.amount = amount
        expenseGroup.payments.append(self)

    def __str__(self):
        return f"{self.date}: {self.payer} paid {self.payee} ${self.amount}."

class User:
    def __init__(self, name, userList):
        self.name = name.lower()
        userList.append(self)

    def __str__(self):
        return f"{self.name.title()}"



