import os

FILE_NAME = "atm.txt"
DEFAULT_PIN = "1234"
DEFAULT_BALANCE = 10000


# Initialize file with default account data
def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as file:
            file.write(DEFAULT_PIN + "\n")
            file.write(str(DEFAULT_BALANCE) + "\n")


# Load account data
def load_data():
    try:
        initialize_file()

        with open(FILE_NAME, "r") as file:
            pin = file.readline().strip()
            balance = int(file.readline().strip())
            transactions = file.readlines()

        return pin, balance, transactions

    except (OSError, ValueError):
        print("File error. Initializing default data.")
        save_data(DEFAULT_PIN, DEFAULT_BALANCE, [])
        return DEFAULT_PIN, DEFAULT_BALANCE, []


# Save account data
def save_data(pin, balance, transactions):
    try:
        with open(FILE_NAME, "w") as file:
            file.write(pin + "\n")
            file.write(str(balance) + "\n")

            for transaction in transactions:
                file.write(transaction)

    except OSError:
        print("Error saving account data.")


# Login with maximum 3 attempts
def login(correct_pin):
    for attempt in range(3):
        entered_pin = input("Enter PIN: ")

        if entered_pin == correct_pin:
            print("Login successful")
            return True

        attempts_left = 2 - attempt

        if attempts_left > 0:
            print(f"Invalid PIN. Attempts left: {attempts_left}")
        else:
            print("Account locked. Exiting...")

    return False


# Check balance
def check_balance(balance):
    print("Current Balance:", balance)


# Deposit money
def deposit(balance, transactions, pin):
    try:
        amount = int(input("Enter deposit amount: "))

        if amount <= 0:
            print("Invalid amount.")
            return balance

        balance += amount

        transactions.append(
            f"Deposit {amount} | Balance: {balance}\n"
        )

        save_data(pin, balance, transactions)

        print(f"Deposit successful. New Balance: {balance}")

        return balance

    except ValueError:
        print("Invalid amount. Please enter numbers only.")
        return balance


# Withdraw money
def withdraw(balance, transactions, pin):
    try:
        amount = int(input("Enter withdrawal amount: "))

        if amount <= 0:
            print("Invalid amount.")

        elif amount > balance:
            print("Insufficient balance.")

        else:
            balance -= amount

            transactions.append(
                f"Withdraw {amount} | Balance: {balance}\n"
            )

            save_data(pin, balance, transactions)

            print(f"Withdrawal successful. New Balance: {balance}")

        return balance

    except ValueError:
        print("Invalid amount. Please enter numbers only.")
        return balance


# Mini statement
def mini_statement(transactions):
    print("\n----- Mini Statement -----")

    if not transactions:
        print("No transactions found.")

    else:
        for transaction in transactions[-5:]:
            print(transaction.strip())

    print("--------------------------")


# Main ATM program
def main():
    pin, balance, transactions = load_data()

    print("===== ATM Management System =====")

    if not login(pin):
        return

    while True:
        print("\n----- ATM MENU -----")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Mini Statement")
        print("5. Exit")

        try:
            choice = input("Enter menu option: ")

            if choice == "1":
                check_balance(balance)

            elif choice == "2":
                balance = deposit(balance, transactions, pin)

            elif choice == "3":
                balance = withdraw(balance, transactions, pin)

            elif choice == "4":
                mini_statement(transactions)

            elif choice == "5":
                save_data(pin, balance, transactions)
                print("Thank you for using ATM.")
                break

            else:
                print("Invalid menu option.")

        except (EOFError, KeyboardInterrupt):
            print("\nProgram terminated.")
            save_data(pin, balance, transactions)
            break


if __name__ == "__main__":
    main()