from pkg import SavingsAccount,CurrentAccount
import json

def main_menu():
    try:
        with open("bank_data.json", "r") as file:
            accounts_data = json.load(file)
    except:
        accounts_data = {}
        
    accounts = {}
    while True:
        print("\nBanking System Menu:")
        print("1. Create Savings Account")
        print("2. Create Current Account")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Display Account Info")
        print("6. Apply Interest (Savings Account)")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            acc_num = input("Enter account number: ")
            name = input("Enter owner name: ")
            accounts[acc_num] = SavingsAccount(acc_num, name, accounts_data.get(acc_num, {}).get("balance", 0))
            print("Savings account created successfully.")
        elif choice == "2":
            acc_num = input("Enter account number: ")
            name = input("Enter owner name: ")
            accounts[acc_num] = CurrentAccount(acc_num, name, accounts_data.get(acc_num, {}).get("balance", 0))
            print("Current account created successfully.")
        elif choice == "3":
            acc_num = input("Enter account number: ")
            if acc_num in accounts:
                amount = float(input("Enter deposit amount: "))
                accounts[acc_num].deposit(amount)
            else:
                print("Account not found.")
        elif choice == "4":
            acc_num = input("Enter account number: ")
            if acc_num in accounts:
                amount = float(input("Enter withdrawal amount: "))
                accounts[acc_num].withdraw(amount)
            else:
                print("Account not found.")
        elif choice == "5":
            acc_num = input("Enter account number: ")
            if acc_num in accounts:
                accounts[acc_num].display_info()
            else:
                print("Account not found.")
        elif choice == "6":
            acc_num = input("Enter account number: ")
            if acc_num in accounts and isinstance(accounts[acc_num], SavingsAccount):
                accounts[acc_num].apply_interest()
            else:
                print("Invalid account or not a savings account.")
        elif choice == "7":
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
