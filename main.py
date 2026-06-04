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

from trackerStrings import intro
from trackerClasses import *

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

#def getValidDate():

#def getValidDollarAmt():


def addGroup(groupsList, userList):
    name = getValidName("\nPlease enter the expense group name: ")
    existingGroupNames = [group.name for group in groupsList]
    while name in existingGroupNames:
        print("That group name is already in use.")
        name = getValidName("Please choose a new name: ")
    newGroup = ExpenseGroup(name)
    addGroupMembers(newGroup, userList)
    groupsList.append(newGroup)
    print("The following expense group was created:")
    print("  " + str(newGroup))
    return newGroup

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
            if group.name.lower() == choice:
                return group
        print("Sorry, that group name does not exist.")

def chooseFunction(functions):
    invalid = True
    trackerOptions = "\nWhat would you like to do? Please enter a number from the following options:\n"
    for i in range(len(functions)):
        trackerOptions += f"{i+1}. {functions[i]}\n"

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

def addGroupMembers(expenseGroup, userList):
    groupMemberList = expenseGroup.members
    newMembers = input("Please enter group members, separated by commas: ")
    parsedNames = [name.strip() for name in newMembers.split(',')]
    existingMemberNames = [member.name for member in groupMemberList]
    newMemberNames = []
    duplicates = []
    newUserNames = []
    for name in parsedNames:
        if name:
            if name not in existingMemberNames and name not in newMemberNames:
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
                groupMemberList.append(user)
                existingUser = True
        if not existingUser:
            newUser = User(name)
            userList.append(newUser)
            groupMemberList.append(newUser)
            newUserNames.append(name)
    if newUserNames:
        print("The following users were not yet in the system and were added:")
        for name in newUserNames:
            print(f"  {name}")

#def addExpense():

#def printExpenses():

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
    allUsers = []
    groups = []
    while running:
        if not groups:
            print("You do not have any expense groups. Please create one to start tracking expenses.")
            currentGroup = addGroup(groups, allUsers)

        else:
            showAllGroups(groups)
            invalid = True
            while invalid:
                option = input("\nWhat would you like to do:\n1. Choose existing group.\n2. Create a new group.\n")
                if option == "1":
                    currentGroup = chooseGroup(groups)
                    invalid = False
                elif option == "2":
                    currentGroup = addGroup(groups, allUsers)
                    showAllGroups(groups)
                else:
                    print("Invalid choice. Please type the number of one of the options.")

        showCurrentGroup(currentGroup)
        groupChosen = True
        while groupChosen:
            choice = chooseFunction(TRACKER_FUNCTIONS)
            if choice == "Add group member(s).":
                print("")
                addGroupMembers(currentGroup, allUsers)
                print("The following expense group has been updated:")
                print("  " + str(currentGroup))
            elif choice == "Add an expense.":
                addExpense()
            elif choice == "Print a report of all expenses.":
                printExpenses()
            elif choice == "Show all balances":
                printBalances()
            elif choice == "Record a payment.":
                recordPayment()
            elif choice == "See all groups.":
                groupChosen = False
            elif choice == "Exit.":
                groupChosen = False
                running = False

if __name__ == "__main__":
    main()


