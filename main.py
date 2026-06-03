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
# Import statements here
from urllib import response

from strings import intro

# Constants
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
    response = ""
    while not response:
        response = input(prompt)
        if 

def getValidDate():

def getValidDollarAmt():

def addGroup(groupList):

def showAllGroups(groupList):

def showCurrentGroup(group):

def chooseGroup(groupList):

def chooseFunction(functions):
    invalid = True
    trackerOptions = "What would you like to do? Please enter a number from the following options:\n"
    for i in functions:
        trackerOptions += f"{i+1}. {functions[i]}\n"

    while invalid:
        try:
            userChoice = int(input(trackerOptions)) - 1
            if userChoice in range(1,len(functions) + 1):
                invalid = False
            else:
                print("Invalid choice. Please try again.\n")
        except ValueError:
            print("Invalid choice. Please enter a number.\n")

    return functions[userChoice]

def addGroupMembers():

def addExpense():

def printExpenses():

# 1. Add an expense

# 2. Print report of all expenses

# 3. Show all balances

# 4. Record a payment

# Check for existing participant and add one if they don't exist


def main():

    # Print intro
    print(intro)

    # Create a group
    running = True
    groups = []
    while running:
        if not groups:
            answer = getYesNoAnswer("You do not have any expense groups. Would you like to create one? (Y/N): ")
            if answer:
                addGroup(groups)
            else:
                running = False

        showAllGroups(groups)

        currentGroup = chooseGroup(groups)

        showCurrentGroup(currentGroup)

        choice = chooseFunction(TRACKER_FUNCTIONS)
        if choice == "Add group member(s).":
            addGroupMembers()
        elif choice == "Add an expense.":
            addExpense()
        elif choice == "Print a report of all expenses.":
            printExpenses()
        elif choice == "Show all balances":
            printBalances()
        elif choice == "Record a payment.":
            recordPayment()
        elif choice == "Exit.":
            running = False
        # Choice "See all groups" will loop back to "while running"

if __name__ == "__main__":
    main()


