import json
import os


DATA_FILE = "pocketiq_data.json"

categories = [
    "Food",
    "Transport",
    "Housing",
    "Entertainment",
    "Shopping",
    "Bills",
    "Healthcare",
    "Other"
]


def save_data():
    data = {
        "income": income,
        "expenses": expenses
    }

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_data():
    if not os.path.exists(DATA_FILE):
        return 0.0, []

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        saved_income = data.get("income", 0.0)
        saved_expenses = data.get("expenses", [])

        return saved_income, saved_expenses

    except (json.JSONDecodeError, OSError):
        print("Saved data could not be loaded. Starting with empty data.")
        return 0.0, []


income, expenses = load_data()


def calculate_total_expenses():
    total = 0.0

    for expense in expenses:
        total += expense[2]

    return total


def display_dashboard():
    total_expenses = calculate_total_expenses()
    remaining_budget = income - total_expenses

    print("\n" + "=" * 40)
    print("PocketIQ".center(40))
    print("=" * 40)
    print(f"Monthly income:    £{income:.2f}")
    print(f"Total expenses:    £{total_expenses:.2f}")
    print(f"Remaining budget:  £{remaining_budget:.2f}")
    print("-" * 40)
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Summary")
    print("4. Delete Expense")
    print("5. Edit Expense")
    print("6. Exit")


while True:
    display_dashboard()
    choice = input("Choose an option: ")

    if choice == "1":
        try:
            income = float(input("Enter your monthly income: £"))

            if income < 0:
                print("Income cannot be negative.")
                continue

            save_data()
            print(f"Monthly income saved: £{income:.2f}")

        except ValueError:
            print("Please enter a valid number.")

    elif choice == "2":
        print("\n" + "=" * 40)
        print("Select Category".center(40))
        print("=" * 40)

        for index, category in enumerate(categories, start=1):
            print(f"{index}. {category}")

        try:
            category_choice = int(input("Choose a category: "))

            if not 1 <= category_choice <= len(categories):
                print("Invalid category.")
                continue

            category = categories[category_choice - 1]
            description = input("Expense description: ").strip()

            if description == "":
                print("Description cannot be empty.")
                continue

            amount = float(input("Expense amount: £"))

            if amount <= 0:
                print("Expense amount must be greater than zero.")
                continue

            expenses.append((category, description, amount))
            save_data()

            print(
                f"Added {description} under {category} "
                f"for £{amount:.2f}"
            )

        except ValueError:
            print("Please enter a valid number.")

    elif choice == "3":
        print("\n" + "=" * 40)
        print("Summary".center(40))
        print("=" * 40)

        if len(expenses) == 0:
            print("No expenses recorded yet.")
            print('Start by choosing "2. Add Expense".')
            print(f"Remaining budget: £{income:.2f}")

        else:
            for index, expense in enumerate(expenses, start=1):
                category = expense[0]
                description = expense[1]
                amount = expense[2]

                print(
                    f"{index}. "
                    f"{description:<15} "
                    f"{category:<15} "
                    f"£{amount:.2f}"
                )

            total_expenses = calculate_total_expenses()
            remaining_budget = income - total_expenses
            number_of_expenses = len(expenses)
            average_expense = total_expenses / number_of_expenses

            largest_expense = max(
                expenses,
                key=lambda expense: expense[2]
            )

            smallest_expense = min(
                expenses,
                key=lambda expense: expense[2]
            )

            print("-" * 40)
            print(f"Total spent:       £{total_expenses:.2f}")
            print(f"Remaining:         £{remaining_budget:.2f}")
            print(f"Expenses logged:   {number_of_expenses}")
            print(f"Average expense:   £{average_expense:.2f}")
            print(
                f"Largest expense:   "
                f"{largest_expense[1]} "
                f"(£{largest_expense[2]:.2f})"
            )
            print(
                f"Smallest expense:  "
                f"{smallest_expense[1]} "
                f"(£{smallest_expense[2]:.2f})"
            )

    elif choice == "4":
        if len(expenses) == 0:
            print("No expenses to delete.")

        else:
            print("\n" + "=" * 40)
            print("Delete Expense".center(40))
            print("=" * 40)

            for index, expense in enumerate(expenses, start=1):
                print(
                    f"{index}. "
                    f"{expense[1]:<15} "
                    f"{expense[0]:<15} "
                    f"£{expense[2]:.2f}"
                )

            try:
                expense_number = int(
                    input(
                        "Enter the expense number to delete "
                        "or 0 to cancel: "
                    )
                )

                if expense_number == 0:
                    print("Deletion cancelled.")

                elif 1 <= expense_number <= len(expenses):
                    removed_expense = expenses.pop(
                        expense_number - 1
                    )

                    save_data()

                    print(
                        f"Deleted {removed_expense[1]} "
                        f"for £{removed_expense[2]:.2f}"
                    )

                else:
                    print("Invalid expense number.")

            except ValueError:
                print("Please enter a valid number.")

    elif choice == "5":
        if len(expenses) == 0:
            print("No expenses to edit.")

        else:
            print("\n" + "=" * 40)
            print("Edit Expense".center(40))
            print("=" * 40)

            for index, expense in enumerate(expenses, start=1):
                print(
                    f"{index}. "
                    f"{expense[1]:<15} "
                    f"{expense[0]:<15} "
                    f"£{expense[2]:.2f}"
                )

            try:
                expense_number = int(
                    input(
                        "Enter the expense number to edit "
                        "or 0 to cancel: "
                    )
                )

                if expense_number == 0:
                    print("Editing cancelled.")
                    continue

                if not 1 <= expense_number <= len(expenses):
                    print("Invalid expense number.")
                    continue

                selected_expense = expenses[expense_number - 1]

                new_description = input(
                    f"New description [{selected_expense[1]}]: "
                ).strip()

                new_amount = input(
                    f"New amount [{selected_expense[2]:.2f}]: £"
                ).strip()

                if new_description == "":
                    new_description = selected_expense[1]

                if new_amount == "":
                    updated_amount = selected_expense[2]

                else:
                    updated_amount = float(new_amount)

                    if updated_amount <= 0:
                        print(
                            "Expense amount must be greater "
                            "than zero."
                        )
                        continue

                expenses[expense_number - 1] = (
                    selected_expense[0],
                    new_description,
                    updated_amount
                )

                save_data()
                print("Expense updated successfully.")

            except ValueError:
                print("Please enter a valid number.")

    elif choice == "6":
        save_data()
        print("Thank you for using PocketIQ!")
        break

    else:
        print("Invalid option. Please try again.")