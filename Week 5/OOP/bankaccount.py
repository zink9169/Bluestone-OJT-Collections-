class Account:
    def __init__(self, acc_number, owner, balance=0.0):
        self.acc_number = acc_number
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
            return True
        print("Insufficient funds or invalid amount.")
        return False

    def __str__(self):
        return f"[{self.__class__.__name__}] ID: {self.acc_number} | Owner: {self.owner} | Balance: ${self.balance:.2f}"


class SavingsAccount(Account):
    def apply_interest(self):
        interest = self.balance * 0.08
        self.balance += interest
        print(f"Interest of 8% (${interest:.2f}) added to Savings {self.acc_number}.")


class DepositAccount(Account):
    def apply_interest(self):
        interest = self.balance * 0.07
        self.balance += interest
        print(f"Interest of 7% (${interest:.2f}) added to Deposit {self.acc_number}.")


class Bank:
    def __init__(self):
        self.accounts = {}

    def open_account(self, acc_type, acc_number, owner, initial_balance):
        if acc_number in self.accounts:
            print("Account number already exists!")
            return

        if acc_type == "1":
            new_acc = SavingsAccount(acc_number, owner, initial_balance)
        else:
            new_acc = DepositAccount(acc_number, owner, initial_balance)

        self.accounts[acc_number] = new_acc
        print(f"Account for {owner} opened successfully.")

    def close_account(self, acc_number):
        if acc_number in self.accounts:
            del self.accounts[acc_number]
            print(f"Account {acc_number} closed.")
        else:
            print("Account not found.")

    def find_account(self, acc_number):
        return self.accounts.get(acc_number)

    def transfer(self, sender_id, receiver_id, amount):
        sender = self.find_account(sender_id)
        receiver = self.find_account(receiver_id)

        if sender and receiver:
            if sender.withdraw(amount):
                receiver.deposit(amount)
                print("Transfer successful.")
        else:
            print("One or both accounts not found.")

    def add_interest_to_all_savings(self):
        for acc in self.accounts.values():
            if isinstance(acc, SavingsAccount):
                acc.apply_interest()



def main():
    my_bank = Bank()

    while True:
        print("\n--- Bank Management System ---")
        print("1. Open Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Funds")
        print("5. Display Account Info")
        print("6. Add Interest (Savings)")
        print("7. Close Account")
        print("8. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            t = input("Type (1: Savings (8%), 2: Deposit (7%)): ")
            num = input("Account Number: ")
            name = input("Owner Name: ")
            bal = float(input("Initial Deposit: "))
            my_bank.open_account(t, num, name, bal)

        elif choice == '2':
            num = input("Account Number: ")
            acc = my_bank.find_account(num)
            if acc:
                acc.deposit(float(input("Amount: ")))
            else:
                print("Not found.")

        elif choice == '3':
            num = input("Account Number: ")
            acc = my_bank.find_account(num)
            if acc:
                acc.withdraw(float(input("Amount: ")))
            else:
                print("Not found.")

        elif choice == '4':
            s = input("From Account #: ")
            r = input("To Account #: ")
            amt = float(input("Amount: "))
            my_bank.transfer(s, r, amt)

        elif choice == '5':
            num = input("Account Number: ")
            acc = my_bank.find_account(num)
            print(acc if acc else "Account not found.")

        elif choice == '6':
            my_bank.add_interest_to_all_savings()

        elif choice == '7':
            num = input("Account Number to close: ")
            my_bank.close_account(num)

        elif choice == '8':
            print("Exiting...")
            break


if __name__ == "__main__":
    main()