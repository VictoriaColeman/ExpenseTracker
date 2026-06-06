from datetime import datetime

# ---------------------------Data Validation---------------------------

def getYesNoAnswer(prompt):
    """
    Gets response to a yes/no question from the user. If there is a 'y'
    in the response, interprets as yes. If there is a 'n' in response,
    interprets as no. Otherwise, continues to prompt.
    :param prompt: string, prompt used to get input
    :return: True if answer is yes, False if answer is no
    """
    invalid = True
    while invalid:
        response = input(prompt).lower()
        if 'y' in response and 'n' not in response:
            return True
        elif 'n' in response:
            return False
        else:
            print("Invalid response. Please enter Y or N.")

def getValidName(prompt):
    """
    Gets non-empty string from the user. Re-prompts if user returns
    empty string.
    :param prompt: string to use as prompt
    :return: returns user inputted-string
    """
    response = input(prompt)
    while not response:
        response = input("Name cannot be blank. " + prompt)
    return response

def getValidDate(prompt):
    """
    Gets a date from the user in the form MM/DD/YYYY. Uses datetime
    module to validate format.
    :param prompt: string, prompt used to get input.
    :return: string, date formatted as "MM/DD/YYYY"
    """
    invalid = True
    while invalid:
        date = input(prompt)
        try:
            date = datetime.strptime(date, "%m/%d/%Y")
            invalid = False
        except ValueError:
            print("Date not properly Formated. ", end="")
    return date.strftime("%m/%d/%Y")

def getValidDollarAmt(prompt):
    """
    Gets a valid dollar amount from the user. Will strip any leading
    dollar sign, spaces, or 0's and round entry to 2 decimal places.
    :param prompt: string, prompt used to get input
    :return: float, rounded to two decimal places
    """
    invalid = True
    while invalid:
        amount = input(prompt).lstrip(" $").replace(',', '')
        try:
            amount = float(amount)
            if amount > 0:
                invalid = False
            else:
                print("Invalid response. Amount must be a positive "
                      "value. ", end="")
        except ValueError:
            print("Invalid characters entered. ", end="")
    return round(amount, 2)

# -----------------------Expense Group Management----------------------

class Tracker:
    """
    Tracker class is the main class for the expense tracker. A
    tracker object has ExpenseGroup objects.
    """
    def __init__(self):
        self.groups = []
        print("You do not have any expense groups. Please create "
              "one to start tracking expenses.")
        self.currentGroup = None
        self.addGroup()

    def addGroup(self):
        """
        Prompts user to create an expense group. Validates that name is
        not empty and a group with the same name does not already exist.
        Sets the new expense group to be the current group.
        :return: None
        """
        existingGroupNames = [group.name for group in self.groups]
        invalid = True
        while invalid:
            name = getValidName("\nPlease enter the expense group "
                                "name: ").lower()
            if name not in existingGroupNames:
                invalid = False
            else:
                print("That group name is already in use.")
        newGroup = ExpenseGroup(name)
        self.groups.append(newGroup)
        self.currentGroup = newGroup

    def showAllGroups(self):
        """
        Prints a list of all existing expense groups with a heading.
        :return: None
        """
        print("\nExisting expense groups:")
        for group in self.groups:
            print("  " + str(group))

    def chooseGroup(self):
        """
        Prompts user to choose an expense group to work with. Validates
        that the group exists.
        :return: None
        """
        invalid = True
        while invalid:
            choice = input("\nWhich expense group would you like to work "
                           "with?: ").lower()
            for group in self.groups:
                if group.name == choice:
                    self.currentGroup = group
                    invalid = False
            if invalid:
                print("Sorry, that group name does not exist.")

class ExpenseGroup:
    """
    ExpenseGroup objects belong to Tracker objects and have Expense,
    Debt, Payment, and User objects.
    """
    def __init__(self, name):
        self.name = name.lower()
        self.members = []
        self.expenses = []
        self.debts = []
        self.payments = []
        self.addGroupMembers()
        print("The following expense group was created:")
        print("  " + str(self))

    def __str__(self):
        memberNames = [user.name.title() for user in self.members]
        return (f"Group: {self.name.title()}, Members: "
                f"{", ".join(memberNames)}")

    def showCurrentGroup(self):
        """
        Prints the expense group the user is currently working with,
        with a header.
        :return: None
        """
        print("\nYou are working with the following expense group:")
        print("  " + str(self))

    def addGroupMembers(self):
        """
        Prompts user to enter names of group members to add to an
        expense group. Validates that the user(s) are not already in
        the group.
        :return: None
        """
        newMembers = input("Please enter group members, separated by "
                           "commas: ")
        parsedNames = [name.strip().lower() for name
                       in newMembers.split(',')]
        currentMemberNames = [member.name for member in self.members]
        newMemberNames = []
        duplicates = []
        for name in parsedNames:
            if name: # Skip empty entries
                if (name not in currentMemberNames
                        and name not in newMemberNames):
                    newMemberNames.append(name)
                else:
                    duplicates.append(name)
        if duplicates:
            print("The following users are already in this group and "
                  "will not be added:")
            for duplicate in duplicates:
                print(f"  {duplicate.title()}")
        for name in newMemberNames:
            self.members.append(User(name))

    def checkForExistingMember(self, name):
        existingGroupMember = False
        for member in self.members:
            if member.name == name.lower():
                user = member
                existingGroupMember = True
        if existingGroupMember:
            return user
        else:
            addMember = getYesNoAnswer(f"{name.title()} is not a member"
                                       f" in this expense group. Would "
                                       f"you like to add them? (Y/N): ")
            if addMember:
                newUser = User(name)
                self.members.append(newUser)
                return newUser
            else:
                return None

    def getExistingMember(self, prompt):
        """
        Will prompt the user to enter the name of an existing group
        member. Will continue to prompt until an existing group
        member is chosen.
        :param prompt: string to prompt user
        :return: User object
        """
        existingMember = False
        while not existingMember:
            user = input(prompt).lower()
            for member in self.members:
                if member.name == user:
                    existingMember = True
                    user = member
            if not existingMember:
                print("That is not an existing group member. Please "
                      "choose an existing member.")
        return user

    def addExpense(self):
        """
        Allows user to enter an expense. Prompts user to enter a valid
        date, non-empty string name, and enter a valid dollar amount.
        Will prompt user to enter the user who paid and validate that
        they are a member of the expense group or that the user wants to
        add them to the group. Adds expense to expense group's
        expense list. Creating the Expense object will prompt user to
        enter participants. Will print a string confirming that the
        expense was created.
        :return: None
        """
        date = getValidDate("\nPlease enter the expense date ("
                            "MM/DD/YYY): ")
        name = getValidName("Please enter the expense description: ")
        amount = getValidDollarAmt("Please enter the expense amount: ")
        payer = None
        while payer is None:
            payerName = getValidName("Who paid?: ")
            payer = self.checkForExistingMember(payerName)
            if payer is None:
                print("User must be in the expense group to pay for an "
                      "expense. Please try again.")
        newExpense = Expense(date, name, amount, payer, self)
        self.expenses.append(newExpense)
        print("The following expense was created:")
        print("  " + str(newExpense))

    def printExpenses(self):
        """
        Prints a list of all existing expenses for the expense group
        with a header.
        :return: None
        """
        print(f"\nDisplaying all expenses for: {self.name.title()}")
        for expense in self.expenses:
            print("  " + str(expense))

    def printPayments(self):
        """
        Prints a list of all existing payments for the expense group
        with a header.
        :return: None
        """
        print(f"\nDisplaying all payments for: {self.name.title()}")
        for payment in self.payments:
            print("  " + str(payment))

    def printBalances(self):
        """
        Prints a list of all remaining balances for the expense group
        with a header.
        :return: None
        """
        print(f"\nDisplaying all balances for: {self.name.title()}")
        for debt in self.debts:
            print("  " + str(debt))

    def recordPayment(self):
        """
        Prompts the user to enter a payment. Validates that the payer
        owes the payee and that the amount paid is not greater than the
        amount owed. If payment reduces a balance to zero,
        the balance is removed from the expense group debts.
        :return: None
        """
        date = getValidDate("\nPayment date (MM/DD/YYYY): ")
        payer = self.getExistingMember("Who made the payment?: ")
        payee = self.getExistingMember("Who received the payment?: ")
        invalidTransaction = False
        if payer == payee:
            print("Invalid payment. Payer and recipient cannot be the "
                  "same. Please try again.")
            invalidTransaction = True
        if not invalidTransaction:
            invalidTransaction = True
            for debt in self.debts:
                if (debt.creditor == payee and debt.debtor == payer
                        and debt.amount > 0):
                    invalidTransaction = False
        if invalidTransaction:
            print(f"Invalid payment. {payer} does not owe {payee} "
                  f"anything. Payment not recorded.")
        else:
            validAmount = False
            while not validAmount:
                payment = getValidDollarAmt("Payment amount: ")
                for debt in self.debts:
                    if (debt.creditor == payee and debt.debtor == payer
                            and payment <= debt.amount):
                        validAmount = True
                        debt.amount -= payment
                        if debt.amount == 0:
                            self.debts.remove(debt)
                if not validAmount:
                    print("That is not a valid amount. Amount paid"
                          " cannot be greater than amount owed. Please"
                          " try again.")
            newPayment = Payment(date, payer, payee, payment, self)
            print(f"The following payment was recorded:\n"
                  f"  {newPayment}")

class Expense:
    """
    Expense objects belong to an ExpenseGroup object and have User
    objects. Creation of an Expense generates and updates Debt objects
    that belong to the ExpenseGroup object
    """
    def __init__(self, date, name, amount, payer, expenseGroup):
        self.date = date
        self.name = name
        self.amount = amount
        self.payer = payer
        self.participants = self.getParticipants(expenseGroup)
        self.createDebts(expenseGroup)
        self.cancelDebts(expenseGroup)

    def __str__(self):
        participants = [participant.name.title() for participant in
                        self.participants]
        return (f"{self.date}: {self.payer} paid ${self.amount} for"
                f" {self.name}. Expense split by:"
                f" {", ".join(participants)}")

    def getParticipants(self, expenseGroup):
        """
        Prompts user to enter a list of participants who will split
        the expense. Checks whether participants exist in the expense
        group. Prompts user to add them if they are not members of the
        group.
        :param expenseGroup: ExpenseGroup object where expense will be '
            recorded
        :return: list of user objects, participants in the expense
        """
        response = input("Please enter all participants who should "
                         "split the expense separated by commas "
                         "(including payer if applicable): ")
        parsedNames = [name.strip().lower() for name in
                       response.split(',')]
        participants = []
        for name in parsedNames:
            user = expenseGroup.checkForExistingMember(name)
            if user and user not in participants:
                participants.append(user)
        return participants

    def createDebts(self, expenseGroup):
        """
        Creates Debt ojects which are added to an expense group when
        an expense is created or updates existing debts. Splits
        expenses equally between participants.
        :param expenseGroup: ExpenseGroup object where the debts will be
            added/updated
        :return: None
        """
        share = self.amount/len(self.participants)
        share = round(share, 2)
        for participant in self.participants:
            if participant != self.payer:
                newBalance = True
                for debt in expenseGroup.debts:
                    if (debt.creditor == self.payer
                            and debt.debtor == participant):
                        debt.amount += share
                        newBalance = False
                if newBalance:
                    Debt(self.payer, participant, share, expenseGroup)

    def cancelDebts(self, expenseGroup):
        """
        Looks for pairs of debts where debtor and creditor are
        reversed and cancels out redundant debt between two users.
        :param expenseGroup: ExpenseGroup object with debts to cancel
        :return: None
        """
        cancelDebts = []
        alterDebts = []
        for outerDebt in expenseGroup.debts:
            debtor = outerDebt.debtor
            creditor = outerDebt.creditor
            for innerDebt in expenseGroup.debts:
                if (debtor == innerDebt.creditor
                        and creditor == innerDebt.debtor
                        and innerDebt not in cancelDebts
                        and outerDebt not in cancelDebts):
                    if outerDebt.amount > innerDebt.amount:
                        cancelDebts.append(innerDebt)
                        alterDebts.append((outerDebt, innerDebt.amount))
                    elif innerDebt.amount > outerDebt.amount:
                        cancelDebts.append(outerDebt)
                        alterDebts.append((innerDebt, outerDebt.amount))
                    else:
                        cancelDebts += [innerDebt, outerDebt]
        for debt in cancelDebts:
            expenseGroup.debts.remove(debt)
        for pair in alterDebts:
            debt = pair[0]
            amt = pair[1]
            debt.amount -= amt

class Debt:
    """
    Debt objects belong to ExpenseGroup objects and have User objects.
    """
    def __init__(self, creditor, debtor, amount, expenseGroup):
        self.creditor = creditor
        self.debtor = debtor
        self.amount = amount
        expenseGroup.debts.append(self)

    def __str__(self):
        return (f"{self.debtor} owes {self.creditor} "
                f"${round(self.amount, 2)}.")

class Payment:
    """
    Payment objects belong to ExpenseGroup objects and have User
    objects.
    """
    def __init__(self, date, payer, payee, amount, expenseGroup):
        self.date = date
        self.payer = payer
        self.payee = payee
        self.amount = amount
        expenseGroup.payments.append(self)

    def __str__(self):
        return (f"{self.date}: {self.payer} paid {self.payee} "
                f"${self.amount}.")

class User:
    """
    User objects belong to Debt, Payment, Expense, and ExpenseGroup
    objects.
    """
    def __init__(self, name):
        self.name = name.lower()

    def __str__(self):
        return f"{self.name.title()}"



