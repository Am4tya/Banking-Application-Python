import os
from datetime import datetime

# File paths
CUSTOMER_DATA_FILE = "customer_info.txt"  # Path to the file storing customer information
ADMIN_DATA_FILE = "admin_info.txt"  # Path to the file storing admin informationZ
TRANSACTION_LOG_FILE = "transaction_history.txt"  # Path to the file storing transaction history
STAFF_DATA_FILE = "staff_info.txt"  # Path to the file storing staff information

# Constants
MIN_SAVINGS_BALANCE = 100  # Minimum balance required for a savings account
MIN_CURRENT_BALANCE = 500  # Minimum balance required for a current account


# Function to fetch customer information from the file
def fetch_customer_info():
    if os.path.exists(CUSTOMER_DATA_FILE):
        with open(CUSTOMER_DATA_FILE, 'r') as file:
            return [line.strip().split(',') for line in file.readlines()]  # Reads and returns customer info
    else:
        return []  # Returns an empty list if file doesn't exist


# Function to save customer information to the file
def save_customer_info(data):
    with open(CUSTOMER_DATA_FILE, 'w') as file:
        for entry in data:
            file.write(','.join(entry) + '\n')  # Writes customer info to the file


# Function to record a transaction in the transaction log file
def record_transaction(account_id, transaction_type, amount):
    with open(TRANSACTION_LOG_FILE, 'a') as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp},{account_id},{transaction_type},{amount}\n")  # Appends transaction to the log file


# Function to generate a unique account ID for new customers
def generate_id():
    customer_info = fetch_customer_info()
    if not customer_info:
        return "24000001"  # If no customers exist, returns initial account ID
    else:
        return str(int(customer_info[-1][0]) + 1)  # Generates next account ID based on the last one


# Function to handle deposit operation
def deposit(account_id):
    amount = float(input("Enter the amount to deposit: "))
    if amount <= 0:
        print("Invalid amount. Please enter a positive value.")
        return
    customer_info = fetch_customer_info()
    account_found = False
    for entry in customer_info:
        if entry[0] == account_id:
            account_found = True
            entry[4] = str(float(entry[4]) + amount)  # Updates balance
            save_customer_info(customer_info)
            record_transaction(account_id, "Deposit", amount)
            print("Deposit successful. Your new balance is:", entry[4])
            break
    if not account_found:
        print("Account not found")


# Function to handle withdrawal operation
def withdraw(account_id):
    amount = float(input("Enter the amount to withdraw: "))
    if amount <= 0:
        print("Invalid amount. Please enter a positive value.")
        return
    customer_info = fetch_customer_info()
    account_found = False
    for entry in customer_info:
        if entry[0] == account_id:
            account_found = True
            # Checks if withdrawal amount doesn't violate minimum balance rules
            if float(entry[4]) - amount < (MIN_SAVINGS_BALANCE if entry[2] == "Savings" else MIN_CURRENT_BALANCE):
                print("Insufficient balance to perform withdrawal.")
                return
            entry[4] = str(float(entry[4]) - amount)  # Updates balance
            save_customer_info(customer_info)
            record_transaction(account_id, "Withdrawal", amount)
            print("Withdrawal successful. Your new balance is:", entry[4])
            break
    if not account_found:
        print("Account not found")


# Function to generate statement of account
def generate_statement(account_id, user_type='customer'):
    if user_type == 'customer':
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
    elif user_type == 'admin':
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
    else:
        print("Invalid user type.")
        return

    transactions = []
    with open(TRANSACTION_LOG_FILE, 'r') as file:
        for line in file:
            timestamp, acc_id, transaction_type, amount = line.strip().split(',')
            if acc_id == account_id and start_date <= timestamp <= end_date:
                transactions.append((timestamp, transaction_type, float(amount)))

    if not transactions:
        print("No transactions found for the specified period.")
        return

    total_deposit = sum(amount for _, transaction_type, amount in transactions if transaction_type == "Deposit")
    total_withdrawal = sum(amount for _, transaction_type, amount in transactions if transaction_type == "Withdrawal")

    # Prints statement of account report
    print("Statement of Account Report")
    print(f"Account ID: {account_id}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print("Transactions:")
    for transaction in transactions:
        print(f"{transaction[0]} - {transaction[1]}: {transaction[2]}")
    print(f"Total Deposits: {total_deposit}")
    print(f"Total Withdrawals: {total_withdrawal}")


# Wrapper function for generating customer statement
def customer_generate_statement(account_id):
    generate_statement(account_id)


# Function to handle customer registration
def customer_registration():
    print("Customer Registration")
    name = input("Enter your name: ")
    while True:
        print("Select account type:")
        print("1. Savings")
        print("2. Current")
        account_type_option = input("Enter option: ")
        if account_type_option == '1':
            account_type = "Savings"
            break
        elif account_type_option == '2':
            account_type = "Current"
            break
        else:
            print("Invalid option. Please enter 1 for Savings or 2 for Current.")
    # Generates unique account ID
    account_id = generate_id()
    password = input("Enter your password: ")
    # Saves customer data
    customer_info = fetch_customer_info()
    customer_info.append([account_id, name, account_type, password, "0"])  # 0 balance initially
    save_customer_info(customer_info)
    print(f"Welcome, {name} Registration Successful. Your account ID is: {account_id}\n")



# Function to handle customer login
def customer_login():
    print("Customer Login")
    account_id = input("Enter your account ID: ")
    password = input("Enter your password: ")
    customer_info = fetch_customer_info()
    for entry in customer_info:
        if entry[0] == account_id and entry[3] == password:
            print(f"Welcome back, {entry[1]}")
            print("Login Successful")
            while True:
                print("\n1. Deposit\n2. Withdraw\n3. Statement of Account\n4. Change Password\n5. Logout")
                choice = input("Enter your choice: ")
                if choice == '1':
                    deposit(account_id)
                elif choice == '2':
                    withdraw(account_id)
                elif choice == '3':
                    customer_generate_statement(account_id)  # Calls customer_generate_statement instead
                elif choice == '4':
                    change_password(account_id)
                elif choice == '5':
                    print("Logging out...")
                    return
                else:
                    print("Invalid choice. Please try again.")
            return
    print("Invalid account ID or password")


# Function to load admin information from file
def load_admin_info():
    if os.path.exists(ADMIN_DATA_FILE):
        with open(ADMIN_DATA_FILE, 'r') as file:
            return [line.strip().split(',') for line in file.readlines()]
    else:
        return []


# Function to save admin information to file
def save_admin_info(data):
    with open(ADMIN_DATA_FILE, 'w') as file:
        for entry in data:
            file.write(','.join(entry) + '\n')


# Function to load staff information from file
def load_staff_info():
    if os.path.exists(STAFF_DATA_FILE):
        with open(STAFF_DATA_FILE, 'r') as file:
            return [line.strip().split(',') for line in file.readlines()]
    else:
        return []


# Function to save staff information to file
def save_staff_info(data):
    with open(STAFF_DATA_FILE, 'w') as file:
        for entry in data:
            file.write(','.join(entry) + '\n')


# Function to establish super user (admin)
def establish_super_user():
    if os.path.exists(ADMIN_DATA_FILE):
        return
    with open(ADMIN_DATA_FILE, 'w') as file:
        file.write("admin,admin123\n")


# Function to change password for a customer
def change_password(account_id):
    new_password = input("Enter new password: ")
    confirm_password = input("Confirm new password: ")
    if new_password != confirm_password:
        print("Passwords do not match. Please try again.")
        return

    customer_info = fetch_customer_info()
    for entry in customer_info:
        if entry[0] == account_id:
            entry[3] = new_password
            save_customer_info(customer_info)
            print("Password changed successfully.")
            return
    print("Account not found")


# Function to handle admin login
def admin_login():
    print("Admin Login")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    admin_info = load_admin_info()
    for entry in admin_info:
        if entry[0] == username and entry[1] == password:
            print("Login Successful")
            admin_menu()
            return
    print("Invalid username or password")


# Function to display and handle admin menu
def admin_menu():
    while True:
        print("\nAdmin Menu")
        print("1. Update Staff Details")
        print("2. Add New Staff")
        print("3. Delete Staff")
        print("4. Update Customer Details")
        print("5. Generate Customer Statement")
        print("6. Logout")
        choice = input("Enter your choice: ")
        if choice == '1':
            update_staff_details()
        elif choice == '2':
            add_new_staff()
        elif choice == '3':
            delete_staff()
        elif choice == '4':
            update_customer_details()
        elif choice == '5':
            generate_customer_statement()
        elif choice == '6':
            print("Logging out...")
            return
        else:
            print("Invalid choice. Please try again.")


# Function to update staff details
def update_staff_details():
    print("Updating Staff Details")
    staff_info = load_staff_info()
    staff_id = input("Enter staff ID to update: ")
    for staff in staff_info:
        if staff[0] == staff_id:
            new_name = input("Enter new name: ")
            staff[1] = new_name
            save_staff_info(staff_info)
            print("Staff details updated successfully.")
            return
    print("Staff ID not found.")


# Function to add new staff
def add_new_staff():
    print("Adding New Staff")
    staff_id = input("Enter staff ID: ")
    name = input("Enter name: ")
    with open(STAFF_DATA_FILE, 'a') as file:
        file.write(f"{staff_id},{name}\n")
    print("New staff added successfully.")


# Function to delete staff
def delete_staff():
    print("Deleting Staff")
    staff_info = load_staff_info()
    staff_id = input("Enter staff ID to delete: ")
    for staff in staff_info:
        if staff[0] == staff_id:
            staff_info.remove(staff)
            save_staff_info(staff_info)
            print("Staff deleted successfully.")
            return
    print("Staff ID not found.")


# Function to update customer details
def update_customer_details():
    print("Updating Customer Details")
    account_id = input("Enter customer account ID to update: ")
    customer_info = fetch_customer_info()
    for entry in customer_info:
        if entry[0] == account_id:
            # Prevent updating customer ID and name
            print("Customer ID:", entry[0])
            print("Customer Name:", entry[1])
            # Allow updating other details
            while True:
                print("Select field to update:")
                print("1. Account Type")
                print("2. Password")
                print("3. Return to Admin Menu")
                field_choice = input("Enter option: ")
                if field_choice == '1':
                    # Update account type
                    while True:
                        print("Select Account Type:")
                        print("1. Savings")
                        print("2. Current")
                        account_type_choice = input("Enter option: ")
                        if account_type_choice == '1':
                            entry[2] = "Savings"
                            print("Account type updated to Savings.")
                            break
                        elif account_type_choice == '2':
                            entry[2] = "Current"
                            print("Account type updated to Current.")
                            break
                        else:
                            print("Invalid option. Please enter 1 for Savings or 2 for Current.")
                elif field_choice == '2':
                    # Update password
                    new_password = input("Enter new password: ")
                    entry[3] = new_password
                    save_customer_info(customer_info)
                    print("Password updated successfully.")
                elif field_choice == '3':
                    return
                else:
                    print("Invalid choice. Please try again.")
            save_customer_info(customer_info)
            return
    print("Customer account not found.")


# Function to generate customer statement by admin
def generate_customer_statement():
    print("Generating Customer Statement")
    account_id = input("Enter customer account ID: ")
    generate_statement(account_id, user_type='admin')


# Main function
def main():
    establish_super_user()  # Creates a default admin account if none exists
    initiate_menu()


# Function to display and handle the main menu
def initiate_menu():
    while True:
        print("Welcome to Amatya Banking Service Application")
        print("1. Customer Login")
        print("2. Customer Register")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            customer_login()
        elif choice == '2':
            customer_registration()
        elif choice == '3':
            admin_login()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()  # Calls the main function when the script is executed
