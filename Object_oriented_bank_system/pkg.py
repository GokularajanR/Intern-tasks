import json

class BankAccount:
    def __init__(self, ac_no, name, balance=0):
        self.__ac_no = ac_no
        self.__name = name
        self.__balance = balance
        self.save_data()
   
    def deposit(self, amt):
        if amt > 0:
            self.__balance += amt
            self.save_data()
            print(f"Deposited {amt}. New balance: {self.__balance}")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amt):
        if 0 < amt <= self.__balance:
            self.__balance -= amt
            self.save_data()
            print(f"Withdrawn {amt}. New balance: {self.__balance}")
        else:
            print("Insufficient balance or invalid amt.")

    def get_balance(self):
        return self.__balance

    def display_info(self):
        print(f"Account: {self.__ac_no}, Owner: {self.__name}, Balance: {self.__balance}")

    def save_data(self):
        try:
            with open("bank_data.json", "r") as file:
                data = json.load(file)
        except:
            data = {}
        
        data[self.__ac_no] = {
            "name": self.__name,
            "balance": self.__balance
        }
        
        with open("bank_data.json", "w") as file:
            json.dump(data, file)

class SavingsAccount(BankAccount):
    def __init__(self, ac_no, name, balance=0.0, rate=0.02):
        super().__init__(ac_no, name, balance)
        self.__rate = rate

    def apply_interest(self):
        interest = self.get_balance() * (self.__rate / 12)
        self.deposit(interest)
        print(f"Applied interest: {interest}")

    def withdraw(self, amt):
        super().withdraw(amt)

class CurrentAccount(BankAccount):
    def __init__(self, ac_no, name, balance=0.0, ov_lim=500):
        super().__init__(ac_no, name, balance)
        self.__ov_lim = ov_lim

    def withdraw(self, amt):
        if self.get_balance() - amt >= -self.__ov_lim:
            super().withdraw(amt)
            if self.get_balance() < 0:
                print(f"using overdraft. Remaining limit: {self.__ov_lim + self.get_balance()}")
        else:
            print("overdraft limit exceeded.")