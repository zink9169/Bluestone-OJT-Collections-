
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, Optional, List
from abc import ABC, abstractmethod

@dataclass
class Book:
    book_id: int
    title: str
    author: str
    is_available: bool = True
    borrowed_by_user_id: Optional[int] = None
    due_date: Optional[date] = None

    def borrow(self, user_id: int, due_date: date) -> None:
        if not self.is_available:
            raise ValueError("Book is not available.")
        self.is_available = False
        self.borrowed_by_user_id = user_id
        self.due_date = due_date

    def return_book(self) -> None:
        self.is_available = True
        self.borrowed_by_user_id = None
        self.due_date = None



class User(ABC):
    def __init__(self, user_id: int, name: str) -> None:
        self.user_id = user_id
        self.name = name.strip()
        self.borrowed_book_ids: List[int] = []

    @property
    @abstractmethod
    def max_books_allowed(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def loan_days(self) -> int:
        raise NotImplementedError

    @property
    def role(self) -> str:
        return "USER"

    def can_borrow(self) -> bool:
        return len(self.borrowed_book_ids) < self.max_books_allowed


class Teacher(User):
    @property
    def max_books_allowed(self) -> int:
        return 5

    @property
    def loan_days(self) -> int:
        return 21

    @property
    def role(self) -> str:
        return "TEACHER"


class Student(User):
    @property
    def max_books_allowed(self) -> int:
        return 3

    @property
    def loan_days(self) -> int:
        return 14

    @property
    def role(self) -> str:
        return "STUDENT"




class Library:
    def __init__(self) -> None:
        self.books: Dict[int, Book] = {}
        self.users: Dict[int, User] = {}

        self._next_book_id: int = 1001
        self._next_user_id: int = 5001


    def add_book(self, title: str, author: str) -> Book:
        title = title.strip()
        author = author.strip()
        if not title:
            raise ValueError("Book title cannot be empty.")
        if not author:
            raise ValueError("Author cannot be empty.")

        book = Book(book_id=self._next_book_id, title=title, author=author)
        self.books[book.book_id] = book
        self._next_book_id += 1
        return book

    def register_user(self, role: str, name: str) -> User:
        name = name.strip()
        if not name:
            raise ValueError("User name cannot be empty.")

        role = role.strip().upper()
        uid = self._next_user_id
        self._next_user_id += 1

        if role == "TEACHER":
            user = Teacher(user_id=uid, name=name)
        elif role == "STUDENT":
            user = Student(user_id=uid, name=name)
        else:
            raise ValueError("Invalid role. Use TEACHER or STUDENT.")

        self.users[user.user_id] = user
        return user

    
    def borrow_book(self, user_id: int, book_id: int) -> None:
        user = self._get_user(user_id)
        book = self._get_book(book_id)

        if not user.can_borrow():
            raise ValueError(f"{user.role} can borrow up to {user.max_books_allowed} books only.")

        if not book.is_available:
            raise ValueError("Book is not available.")

        due = date.today() + timedelta(days=user.loan_days)
        book.borrow(user_id=user.user_id, due_date=due)
        user.borrowed_book_ids.append(book.book_id)

    
    def return_book(self, user_id: int, book_id: int) -> bool:
        """
        Returns: True if returned late, False otherwise
        """
        user = self._get_user(user_id)
        book = self._get_book(book_id)

        if book.is_available:
            raise ValueError("This book is not currently borrowed.")
        if book.borrowed_by_user_id != user.user_id:
            raise ValueError("This book was not borrowed by this user.")

        today = date.today()
        due = book.due_date
        is_late = (due is not None) and (today > due)

        book.return_book()
        if book_id in user.borrowed_book_ids:
            user.borrowed_book_ids.remove(book_id)

        return is_late

    
    def show_all_books(self) -> None:
        if not self.books:
            print("No books in library.")
            return

        print("\nAll Books")
        print("-" * 90)
        print(f"{'ID':<8}{'Title':<30}{'Author':<20}{'Available':<12}{'Borrowed By':<12}{'Due Date'}")
        print("-" * 90)

        for b in self.books.values():
            borrowed_by = str(b.borrowed_by_user_id) if b.borrowed_by_user_id else "-"
            due = b.due_date.isoformat() if b.due_date else "-"
            print(f"{b.book_id:<8}{b.title:<30}{b.author:<20}{str(b.is_available):<12}{borrowed_by:<12}{due}")

        print("-" * 90)

    
    def show_all_users(self) -> None:
        if not self.users:
            print("No users registered.")
            return

        print("\nAll Users")
        print("-" * 90)
        print(f"{'ID':<8}{'Name':<25}{'Role':<12}{'Borrowed Count':<15}{'Borrowed Book IDs'}")
        print("-" * 90)

        for u in self.users.values():
            borrowed_ids = ", ".join(str(i) for i in u.borrowed_book_ids) if u.borrowed_book_ids else "-"
            print(f"{u.user_id:<8}{u.name:<25}{u.role:<12}{len(u.borrowed_book_ids):<15}{borrowed_ids}")

        print("-" * 90)

    

    def _get_user(self, user_id: int) -> User:
        u = self.users.get(user_id)
        if not u:
            raise ValueError("User not found.")
        return u

    def _get_book(self, book_id: int) -> Book:
        b = self.books.get(book_id)
        if not b:
            raise ValueError("Book not found.")
        return b


class LibraryApp:
    def __init__(self) -> None:
        self.library = Library()

        self.library.add_book("Clean Code", "Robert C. Martin")
        self.library.add_book("Python Crash Course", "Eric Matthes")
        self.library.register_user("TEACHER", "Teacher One")
        self.library.register_user("STUDENT", "Student One")

    def run(self) -> None:
        while True:
            print("\nTask 1: Library Management")
            print("1. Add Book")
            print("2. Register User")
            print("3. Borrow Book")
            print("4. Return Book")
            print("5. Show All Books")
            print("6. Show All Users")
            print("7. Exit")

            try:
                choice = int(input("Choose: ").strip())
                if choice == 1:
                    self._add_book_flow()
                elif choice == 2:
                    self._register_user_flow()
                elif choice == 3:
                    self._borrow_book_flow()
                elif choice == 4:
                    self._return_book_flow()
                elif choice == 5:
                    self.library.show_all_books()
                elif choice == 6:
                    self.library.show_all_users()
                elif choice == 7:
                    print("Goodbye.")
                    return
                else:
                    print("Invalid option.")
            except ValueError as e:
                print(f"Error: {e}")

    def _add_book_flow(self) -> None:
        title = input("Book title: ").strip()
        author = input("Author: ").strip()
        b = self.library.add_book(title, author)
        print(f"Book added successfully. Book ID: {b.book_id}")

    def _register_user_flow(self) -> None:
        print("User Role: 1) Teacher  2) Student")
        r = input("Choose role: ").strip()
        role = "TEACHER" if r == "1" else "STUDENT" if r == "2" else ""
        name = input("Name: ").strip()
        u = self.library.register_user(role, name)
        print(f"User registered successfully. User ID: {u.user_id} ({u.role})")

    def _borrow_book_flow(self) -> None:
        self.library.show_all_users()
        user_id = int(input("User ID: ").strip())

        self.library.show_all_books()
        book_id = int(input("Book ID to borrow: ").strip())

        self.library.borrow_book(user_id, book_id)
        print("Book borrowed successfully.")

    def _return_book_flow(self) -> None:
        self.library.show_all_users()
        user_id = int(input("User ID: ").strip())

        self.library.show_all_books()
        book_id = int(input("Book ID to return: ").strip())

        late = self.library.return_book(user_id, book_id)
        if late:
            print("Book returned successfully, but it was LATE.")
        else:
            print("Book returned successfully (on time).")


if __name__ == "__main__":
    LibraryApp().run()
