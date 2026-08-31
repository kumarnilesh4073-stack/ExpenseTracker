print("===== EXPENSE TRACKER =====")

while True:
    print("\n1. Add Expense")
    print("2. View Expenses")
    print("3. Show Total")
    print("4. Exit")

    choice = input("\nEnter your choice: ")
    if choice == "1":
        name = input("Enter your name: ")
        amount = float(input("Enter expense amount: "))
        category = input("Enter expense category: ")

        with open("expenses.txt", "a") as file:
            file.write(f"{name} | {amount} | {category}\n")

        print("Expense Saved Successfully!")

   elif choice == "2":
        print("\n===== ALL EXPENSES =====")

        with open("expenses.txt", "r") as file:
            for expense in file:
                print(expense.strip())

    elif choice == "3":
        total = 0

        with open("expenses.txt", "r") as file:
            for expense in file:
                parts = expense.strip().split(" | ")
                total += float(parts[1])

        print("\nTotal Expense:", total)

    elif choice == "4":
        print("Thank you for using Expense Tracker!")
        break

    else:
        print("Invalid choice! Please try again.")
