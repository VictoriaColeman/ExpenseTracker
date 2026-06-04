# ------------------------------------------------------------------------
#
#  Program: Expense Tracker
#
#  Description: This program allows you to record shared expenses and calculate
#           each participants balances.
#
#  Author: Victoria Coleman
#  Created: May 30, 2026
#
# ********NEED TO ADD DOCSTRINGS******************
#
# ------------------------------------------------------------------------

from trackerStrings import intro
from trackerClasses import *
from datetime import datetime

TRACKER_FUNCTIONS = ("Add group member(s).", "Add an expense.", "Print a report of all expenses.", "Show all balances", "Record a payment.", "See all groups.", "Exit.")

def getYesNoAnswer(prompt):
    #returns True if yes, False if no
    invalid = True
    while invalid:
        response = input(prompt).lower()
        if "y" in response:
            return True
        elif "n" in response:
            return False
        else:
            print("Invalid response. Please enter Y or N.")

def getValidName(prompt):
    response = input(prompt)
    while not response:
        response = input("Name cannot be blank. " + prompt)
    return response

def getValidDate(prompt):
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
    invalid = True
    while invalid:
        amount = input(prompt).lstrip(" 0$").rstrip().replace(',', '')
        try:
            amount = float(amount)
            invalid = False
        except ValueError:
            print("Invalid characters entered. ", end="")
    return round(amount, 2)

def addGroup(groupsList, userList):
    completed = False
    while not completed:
        name = getValidName("\nPlease enter the expense group name: ")
        existingGroupNames = [group.name for group in groupsList]
        while name.lower() in existingGroupNames:
            print("That group name is already in use.")
            name = getValidName("Please choose a new name: ")
        newGroup = ExpenseGroup(name, groupsList, userList)
        if newGroup in groupsList:
            return newGroup
        else:
            if not groupsList:
                print("You must create a group to start tracking expenses. Please create an expense group.")
            else:
                completed = True

def showAllGroups(groupList):
    print("\nExisting expense groups:")
    for group in groupList:
        print("  " + str(group))

def showCurrentGroup(group):
    print("\nYou are working with the following expense group:")
    print("  " + str(group))

def chooseGroup(groupList):
    invalid = True
    while invalid:
        choice = input("\nWhich expense group would you like to work with?: ").lower()
        for group in groupList:
            if group.name == choice:
                return group
        print("Sorry, that group name does not exist.")

def chooseFunction(functions):
    invalid = True
    trackerOptions = "\nWhat would you like to do? Please enter a number from the following options:\n"
    for i in range(len(functions)):
        trackerOptions += f"{i+1}. {functions[i]}\n"
    trackerOptions += "Response: "

    while invalid:
        try:
            userChoice = int(input(trackerOptions)) - 1
            if userChoice in range(len(functions)):
                invalid = False
            else:
                print("Invalid choice. Please try again.\n")
        except ValueError:
            print("Invalid choice. Please enter a number.\n")

    return functions[userChoice]

def addExpense(expenseGroup, userList):
    print("")
    date = getValidDate("Please enter the expense date (MM/DD/YYY): ")
    name = getValidName("Please enter the expense description: ")
    amount = getValidDollarAmt("Please enter the expense amount: ")
    payerName = getValidName("Who paid?: ")
    payer = expenseGroup.checkForExistingMember(payerName, userList)
    newExpense = Expense(date, name, amount, payer, expenseGroup, userList)
    print("The following expense was created:")
    print("  " + str(newExpense))

def printExpenses(expenseGroup):
    print(f"\nDisplaying all expenses for: {expenseGroup.name.title()}")
    for expense in expenseGroup.expenses:
        print("  " + str(expense))

def printBalances(expenseGroup):
    print(f"\nDisplaying all balances for: {expenseGroup.name.title()}")
    for debt in expenseGroup.debts:
        print("  " + str(debt))

# 3. Show all balances

# 4. Record a payment

# Check for existing participant and add one if they don't exist


def main():

    # Print intro
    print(intro)

    # Create a group
    running = True
    allUsers = []
    groups = []
    while running:
        if not groups:
            print("You do not have any expense groups. Please create one to start tracking expenses.")
            getGroup = addGroup(groups, allUsers)
            if getGroup != None:
                currentGroup = getGroup

        else:
            showAllGroups(groups)
            invalid = True
            while invalid:
                option = input("\nWhat would you like to do:\n1. Choose existing group.\n2. Create a new group.\nResponse: ")
                if option == "1":
                    currentGroup = chooseGroup(groups)
                    invalid = False
                elif option == "2":
                    newGroup = addGroup(groups, allUsers)
                    if newGroup:
                        currentGroup = newGroup
                    showAllGroups(groups)
                else:
                    print("Invalid choice. Please type the number of one of the options.")

        showCurrentGroup(currentGroup)
        groupChosen = True
        while groupChosen:
            choice = chooseFunction(TRACKER_FUNCTIONS)
            if choice == "Add group member(s).":
                print("")
                currentGroup.addGroupMembers(allUsers)
                print("The following expense group has been updated:")
                print("  " + str(currentGroup))
            elif choice == "Add an expense.":
                addExpense(currentGroup, allUsers)
            elif choice == "Print a report of all expenses.":
                printExpenses(currentGroup)
            elif choice == "Show all balances":
                printBalances(currentGroup)
            elif choice == "Record a payment.":
                currentGroup.recordPayment()
            elif choice == "See all groups.":
                groupChosen = False
            elif choice == "Exit.":
                groupChosen = False
                running = False

if __name__ == "__main__":
    main()


