# ----------------------------------------------------------------------
#
#  Program: Expense Tracker
#
#  Description: This program allows you to create expense groups,
#           record shared expenses and payments, and calculates each
#           participant's balances.
#
#  Author: Victoria Coleman
#  Created: May 30, 2026
#
# ----------------------------------------------------------------------

from trackerStrings import intro
from trackerClasses import Tracker

TRACKER_FUNCTIONS = ("Add group member(s).", "Add an expense.",
                     "Print a report of all expenses.",
                     "Show all balances", "Record a payment.",
                     "See all groups.", "Exit.")

def chooseFunction(functions):
    """
    Asks the user which expense tracker function they would like to
    perform. Prompts user to enter the number of the function and
    validates that response is a number within the allowed range.
    :param functions: list of strings representing tracker functions
    that the user can choose from.
    :return: string from list of available functions representing the
    user's choice.
    """
    invalid = True
    trackerOptions = ("\nWhat would you like to do? Please enter a "
                      "number from the following options:\n")
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

def main():

    # Print intro
    print(intro)

    # Initialize expense tracker - create first expense group
    t = Tracker()

    # Create a group
    running = True
    while running:

        # Show existing expense groups
        t.showAllGroups()

        # Prompt user to either choose existing group or create new one.
        invalid = True
        while invalid:
            option = input("\nWhat would you like to do:"
                           "\n1. Choose existing group."
                           "\n2. Create a new group."
                           "\nResponse: ").strip(" .#")

            if option == "1":
                t.currentGroup = t.chooseGroup()
                invalid = False
            elif option == "2":
                t.addGroup()
                t.showAllGroups()
            else:
                print("Invalid choice. Please type the number of "
                      "one of the options.")

        # Will occur when user chooses "Show all groups"
        else:
            showAllGroups()
            invalid = True
            while invalid:


        # After creating first group or choosing a group to work
        # with, display current group.
        currentGroup.showCurrentGroup()

        # Loop will continue to ask user what function they would
        # like to perform unless they choose "Show all groups" or
        # "Exit."
        groupChosen = True
        while groupChosen:
            choice = chooseFunction(TRACKER_FUNCTIONS)

            # "Add group member(s)."
            if choice == TRACKER_FUNCTIONS[0]:
                currentGroup.addGroupMembers()

            # "Add an expense."
            elif choice == TRACKER_FUNCTIONS[1]:
                currentGroup.addExpense()

            # "Print a report of all expenses."
            elif choice == TRACKER_FUNCTIONS[2]:
                currentGroup.printExpenses()

            # "Show all balances"
            elif choice == TRACKER_FUNCTIONS[3]:
                currentGroup.printBalances()

            # "Record a payment."
            elif choice == TRACKER_FUNCTIONS[4]:
                currentGroup.recordPayment()

            # "See all groups."
            elif choice == TRACKER_FUNCTIONS[5]:
                groupChosen = False

            # "Exit."
            elif choice == TRACKER_FUNCTIONS[6]:
                groupChosen = False
                running = False

if __name__ == "__main__":
    main()


