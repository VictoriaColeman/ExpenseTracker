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

TRACKER_FUNCTIONS = ("Add an expense.", "Record a payment.",
                     "Show all expenses.", "Show all payments.",
                     "Show all balances.", "Add group member(s).",
                     "See all expense groups.", "Exit.")

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
            userChoice = int(input(trackerOptions).strip(" #.")) - 1
            if userChoice in range(len(functions)):
                invalid = False
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid choice. Please enter a number.")

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
                t.chooseGroup()
                invalid = False
            elif option == "2":
                t.addGroup()
                t.showAllGroups()
            else:
                print("Invalid choice. Please type the number of "
                      "one of the options.")

        # Once user has created or chosen a group to work with,
        # displays the active expense group.
        t.currentGroup.showCurrentGroup()

        # Loop will continue to ask user what function they would
        # like to perform with the active expense group unless they
        # choose "Show all groups" or "Exit."
        groupChosen = True
        while groupChosen:
            choice = chooseFunction(TRACKER_FUNCTIONS)

            # "Add an expense."
            if choice == TRACKER_FUNCTIONS[0]:
                t.currentGroup.addExpense()

            # "Record a payment."
            elif choice == TRACKER_FUNCTIONS[1]:
                t.currentGroup.recordPayment()

            # "Show all expenses."
            elif choice == TRACKER_FUNCTIONS[2]:
                t.currentGroup.printExpenses()

            # "Show all payments."
            elif choice == TRACKER_FUNCTIONS[3]:
                t.currentGroup.printPayments()

            # "Show all balances"
            elif choice == TRACKER_FUNCTIONS[4]:
                t.currentGroup.printBalances()

            # "Add group member(s)."
            elif choice == TRACKER_FUNCTIONS[5]:
                print("")
                t.currentGroup.addGroupMembers()
                print("The following expense group has been updated:")
                print("  " + str(t.currentGroup))

            # "See all expense groups."
            elif choice == TRACKER_FUNCTIONS[6]:
                groupChosen = False

            # "Exit."
            elif choice == TRACKER_FUNCTIONS[7]:
                groupChosen = False
                running = False

if __name__ == "__main__":
    main()


