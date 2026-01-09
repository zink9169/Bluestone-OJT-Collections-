
class Account:


    # Account ရဲ ့data ကို class အတွင်းမှာ encapsulate လုပ်ထား
    def __init__(self, acc_no, name, balance):
        self.acc_no = acc_no
        self.name = name
        self.balance = balance

    #ပိုက်ဆံထည့် → balance တိုး
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposit successful. Balance = {self.balance}")

    #ပိုက်ဆံထုတ် → balance စစ်ပြီးလျော့
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Withdraw successful. Balance = {self.balance}")
        else:
            print("Insufficient balance")

    #Account information ပြ
    def display(self):
        print(f"Account No : {self.acc_no}")
        print(f"Name       : {self.name}")
        print(f"Balance    : {self.balance}")


#Inheritance
# SavingsAccount IS-A Account
# acc_no, name, balance
# deposit(), withdraw(), display()
# အားလုံးကို Account ကနေအမွေဆက်ခံ
class SavingsAccount(Account):
    #Savings Account အတွက် 8% interest
    def add_interest(self):
        interest = self.balance * 0.08
        self.balance += interest
        print(f"8% Interest added. New Balance = {self.balance}")

#Inheritance
#Deposit Account လည်း Account ကို inherit လုပ်တယ် ဒါပေမယ့် interest rate မတူ
class DepositAccount(Account):
    #same method name, different behavior
    def add_interest(self):
        interest = self.balance * 0.07
        self.balance += interest
        print(f"7% Interest added. New Balance = {self.balance}")

class Bank:
    def __init__(self):
        #Encapsulation
        #Bank HAS-A list of accounts
        self.accounts = []

#Account object ကို bank ထဲ register လုပ်
    def open_account(self, account):
        self.accounts.append(account)
        print("Account opened successfully")

#Code reusability
    def find_account(self, acc_no):
        for acc in self.accounts:
            if acc.acc_no == acc_no:
                return acc
        return None
    def close_account(self, acc_no):
        acc = self.find_account(acc_no)
        if acc:
            self.accounts.remove(acc)
            print("Account closed successfully")
        else:
            print("Account not found")

#Abstraction
#Bank ကနေတစ်ဆင့် account ကို access
#(User က Account object ကိုတိုက်ရိုက်မကိုင်)
    def deposit(self, acc_no, amount):
        acc = self.find_account(acc_no)
        if acc:
            acc.deposit(amount)
        else:
            print("Account not found")
    def withdraw(self, acc_no, amount):
        acc = self.find_account(acc_no)
        if acc:
            acc.withdraw(amount)
        else:
            print("Account not found")

#Object collaboration
    def transfer(self, from_acc, to_acc, amount):
        sender = self.find_account(from_acc)
        receiver = self.find_account(to_acc)

        if sender and receiver:
            if sender.balance >= amount:
                sender.balance -= amount
                receiver.balance += amount
                print("Transfer successful")
            else:
                print("Insufficient balance")
        else:
            print("Account not found")

    def display_account(self, acc_no):
        acc = self.find_account(acc_no)
        if acc:
            acc.display()
        else:
            print("Account not found")

    def add_interest_savings(self):
        for acc in self.accounts:
            if isinstance(acc, SavingsAccount):
                acc.add_interest()
#bank object
bank = Bank()
#objects
bank.open_account(SavingsAccount(101, "Aung Aung", 1000))
bank.open_account(DepositAccount(201, "Su Su", 2000))


bank.deposit(101, 500)
bank.withdraw(101, 300)


bank.transfer(101, 201, 200)


bank.display_account(101)
bank.display_account(201)

bank.add_interest_savings()


bank.close_account(201)
