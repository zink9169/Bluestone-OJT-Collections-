from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Account:
    account_no: int
    owner: str
    balance: float = 0.0

    @property
    def account_type(self) -> str:
        return "Account"

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be > 0.")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdraw amount must be > 0.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

    def display_info(self) -> None:
        print("-" * 50)
        print(f"Account No : {self.account_no}")
        print(f"Owner      : {self.owner}")
        print(f"Type       : {self.account_type}")
        print(f"Balance    : {self.balance:.2f}")
        print("-" * 50)


class SavingsAccount(Account):
    MONTHLY_INTEREST_RATE = 0.08  

    @property
    def account_type(self) -> str:
        return "Savings"

    def add_monthly_interest(self) -> float:
        """Returns interest added."""
        interest = self.balance * self.MONTHLY_INTEREST_RATE
        self.balance += interest
        return interest


class DepositAccount(Account):
    MONTHLY_INTEREST_RATE = 0.07  

    @property
    def account_type(self) -> str:
        return "Deposit"

    def add_monthly_interest(self) -> float:
        """Optional: If you later want to apply interest to Deposit accounts."""
        interest = self.balance * self.MONTHLY_INTEREST_RATE
        self.balance += interest
        return interest




class Bank:
    def __init__(self) -> None:
        self._accounts: Dict[int, Account] = {}
        self._next_acc_no: int = 1001

    def open_account(self, owner: str, acc_type: str, initial_deposit: float = 0.0) -> Account:
        owner = owner.strip()
        if not owner:
            raise ValueError("Owner name cannot be empty.")
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative.")

        acc_no = self._next_acc_no
        self._next_acc_no += 1

        acc_type = acc_type.lower().strip()
        if acc_type == "savings":
            account = SavingsAccount(account_no=acc_no, owner=owner, balance=initial_deposit)
        elif acc_type == "deposit":
            account = DepositAccount(account_no=acc_no, owner=owner, balance=initial_deposit)
        else:
            raise ValueError("Invalid account type. Use 'savings' or 'deposit'.")

        self._accounts[acc_no] = account
        return account

    def close_account(self, account_no: int) -> None:
        if account_no not in self._accounts:
            raise ValueError("Account not found.")
        del self._accounts[account_no]

    def find_account(self, account_no: int) -> Account:
        acc = self._accounts.get(account_no)
        if not acc:
            raise ValueError("Account not found.")
        return acc

    def deposit_money(self, account_no: int, amount: float) -> None:
        self.find_account(account_no).deposit(amount)

    def withdraw_money(self, account_no: int, amount: float) -> None:
        self.find_account(account_no).withdraw(amount)

    def transfer_funds(self, from_acc_no: int, to_acc_no: int, amount: float) -> None:
        if from_acc_no == to_acc_no:
            raise ValueError("Cannot transfer to the same account.")
        if amount <= 0:
            raise ValueError("Transfer amount must be > 0.")

        from_acc = self.find_account(from_acc_no)
        to_acc = self.find_account(to_acc_no)

        from_acc.withdraw(amount)
        
        to_acc.deposit(amount)

    def display_account_info(self, account_no: int) -> None:
        self.find_account(account_no).display_info()

    def add_interest_to_savings_accounts(self) -> float:
        """Adds monthly interest to ALL savings accounts. Returns total interest added."""
        total_interest = 0.0
        for acc in self._accounts.values():
            if isinstance(acc, SavingsAccount):
                total_interest += acc.add_monthly_interest()
        return total_interest

    def list_all_accounts(self) -> None:
        if not self._accounts:
            print("No accounts in the bank.")
            return
        for acc in self._accounts.values():
            acc.display_info()




class BankApp:
    def __init__(self) -> None:
        self.bank = Bank()

    def run(self) -> None:
        while True:
            print("\nTask 3: Bank Account Management")
            print("1. Open / Close / Find Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Transfer Funds")
            print("5. Display Account Info")
            print("6. Add Interest to Savings Accounts")
            print("7. Exit")

            choice = self._read_int("Choose: ")

            try:
                if choice == 1:
                    self._account_management_menu()
                elif choice == 2:
                    self._deposit_flow()
                elif choice == 3:
                    self._withdraw_flow()
                elif choice == 4:
                    self._transfer_flow()
                elif choice == 5:
                    self._display_flow()
                elif choice == 6:
                    self._add_interest_flow()
                elif choice == 7:
                    print("Goodbye.")
                    return
                else:
                    print("Invalid option.")
            except ValueError as e:
                print(f"Error: {e}")


    def _account_management_menu(self) -> None:
        while True:
            print("\nAccount Management")
            print("1. Open Account")
            print("2. Close Account")
            print("3. Find Account")
            print("4. Back")

            choice = self._read_int("Choose: ")

            try:
                if choice == 1:
                    owner = input("Owner name: ").strip()
                    print("Account Type: 1) Savings  2) Deposit")
                    t = self._read_int("Choose type: ")
                    acc_type = "savings" if t == 1 else "deposit" if t == 2 else ""
                    initial = self._read_float("Initial deposit (0 allowed): ")

                    acc = self.bank.open_account(owner, acc_type, initial)
                    print(f"Account opened successfully. Account No: {acc.account_no}")

                elif choice == 2:
                    acc_no = self._read_int("Account number to close: ")
                    self.bank.close_account(acc_no)
                    print("Account closed successfully.")

                elif choice == 3:
                    acc_no = self._read_int("Account number to find: ")
                    acc = self.bank.find_account(acc_no)
                    acc.display_info()

                elif choice == 4:
                    return
                else:
                    print("Invalid option.")
            except ValueError as e:
                print(f"Error: {e}")

    def _deposit_flow(self) -> None:
        acc_no = self._read_int("Account number: ")
        amount = self._read_float("Deposit amount: ")
        self.bank.deposit_money(acc_no, amount)
        print("Deposit successful.")

    def _withdraw_flow(self) -> None:
        acc_no = self._read_int("Account number: ")
        amount = self._read_float("Withdraw amount: ")
        self.bank.withdraw_money(acc_no, amount)
        print("Withdraw successful.")

    def _transfer_flow(self) -> None:
        from_acc = self._read_int("From account number: ")
        to_acc = self._read_int("To account number: ")
        amount = self._read_float("Transfer amount: ")
        self.bank.transfer_funds(from_acc, to_acc, amount)
        print("Transfer successful.")

    def _display_flow(self) -> None:
        acc_no = self._read_int("Account number: ")
        self.bank.display_account_info(acc_no)

    def _add_interest_flow(self) -> None:
        total = self.bank.add_interest_to_savings_accounts()
        print(f"Interest added to savings accounts. Total interest added: {total:.2f}")


    @staticmethod
    def _read_int(prompt: str) -> int:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            raise ValueError("Please enter a valid integer.")

    @staticmethod
    def _read_float(prompt: str) -> float:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            raise ValueError("Please enter a valid number.")


if __name__ == "__main__":
    BankApp().run()
