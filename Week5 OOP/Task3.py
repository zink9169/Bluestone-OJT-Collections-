# -- Account Class --
class Account:
    def __init__(self, acc_no, name, balance):
        self.acc_no = acc_no
        self.name = name
        self.balance = float(balance)

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid amount.")
            return
        self.balance += amount
        print("Deposit successful.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid amount.")
            return
        if amount > self.balance:
            print("Insufficient balance.")
            return
        self.balance -= amount
        print("Withdrawal successful.")

    def display(self):
        print(f"Account No: {self.acc_no}")
        print(f"Name      : {self.name}")
        print(f"Balance   : {self.balance:.2f}")


# -- Savings Account --
class SavingsAccount(Account):
    INTEREST_RATE = 0.08

    def add_interest(self):
        interest = self.balance * self.INTEREST_RATE
        self.balance += interest
        print("8% interest added.")


# -- Deposit Account --
class DepositAccount(Account):
    INTEREST_RATE = 0.07

    def add_interest(self):
        interest = self.balance * self.INTEREST_RATE
        self.balance += interest
        print("7% interest added.")


# -- Bank Class --
class Bank:
    def __init__(self):
        self.accounts = []

    def open_account(self):
        acc_no = len(self.accounts) + 1
        name = input("Enter customer name: ")

        print("1. Savings Account (8%)")
        print("2. Deposit Account (7%)")
        acc_type = input("Choose account type: ")

        try:
            balance = float(input("Enter initial balance: "))
        except:
            print("Invalid balance.")
            return

        if acc_type == "1":
            acc = SavingsAccount(acc_no, name, balance)
        elif acc_type == "2":
            acc = DepositAccount(acc_no, name, balance)
        else:
            print("Invalid account type.")
            return

        self.accounts.append(acc)
        print("Account opened successfully!")
        print("Account Number:", acc_no)

    def close_account(self):
        try:
            acc_no = int(float(input("Enter account number to close: ")))
        except:
            print("Invalid input.")
            return

        for acc in self.accounts:
            if acc.acc_no == acc_no:
                self.accounts.remove(acc)
                print("Account closed successfully.")
                return

        print("Account not found.")

    def find_account(self, acc_no):
        for acc in self.accounts:
            if acc.acc_no == acc_no:
                return acc
        return None

    def deposit_money(self):
        try:
            acc_no = int(float(input("Enter account number: ")))
        except:
            print("Invalid input.")
            return

        acc = self.find_account(acc_no)
        if not acc:
            print("Account not found.")
            return

        try:
            amount = float(input("Enter amount: "))
        except:
            print("Invalid amount.")
            return

        acc.deposit(amount)

    def withdraw_money(self):
        try:
            acc_no = int(float(input("Enter account number: ")))
        except:
            print("Invalid input.")
            return

        acc = self.find_account(acc_no)
        if not acc:
            print("Account not found.")
            return

        try:
            amount = float(input("Enter amount: "))
        except:
            print("Invalid amount.")
            return

        acc.withdraw(amount)

    def transfer_funds(self):
        try:
            from_acc_no = int(float(input("From account number: ")))
            to_acc_no = int(float(input("To account number: ")))
        except:
            print("Invalid account number.")
            return

        from_acc = self.find_account(from_acc_no)
        to_acc = self.find_account(to_acc_no)

        if not from_acc or not to_acc:
            print("Invalid account number.")
            return

        try:
            amount = float(input("Enter transfer amount: "))
        except:
            print("Invalid amount.")
            return

        if amount <= 0 or amount > from_acc.balance:
            print("Transfer not possible.")
            return

        from_acc.withdraw(amount)
        to_acc.deposit(amount)
        print("Transfer successful.")

    def display_account(self):
        try:
            acc_no = int(float(input("Enter account number: ")))
        except:
            print("Invalid input.")
            return

        acc = self.find_account(acc_no)
        if acc:
            acc.display()
        else:
            print("Account not found.")

    def add_interest_to_savings(self):
        for acc in self.accounts:
            if isinstance(acc, SavingsAccount):
                acc.add_interest()
        print("Interest added to all savings accounts.")


# -- MAIN PROGRAM --
bank = Bank()

while True:
    print("\n===== BANK ACCOUNT MANAGEMENT =====")
    print("1. Open Account")
    print("2. Close Account")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Transfer Funds")
    print("6. Display Account Info")
    print("7. Add Interest to Savings Accounts")
    print("8. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        bank.open_account()
    elif choice == "2":
        bank.close_account()
    elif choice == "3":
        bank.deposit_money()
    elif choice == "4":
        bank.withdraw_money()
    elif choice == "5":
        bank.transfer_funds()
    elif choice == "6":
        bank.display_account()
    elif choice == "7":
        bank.add_interest_to_savings()
    elif choice == "8":
        print("Thank you! Exiting...")
        break
    else:
        print("Invalid choice!")
