from datetime import date

# Book Class
class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_available = True

    def borrow(self):
        self.is_available = False

    def return_book(self):
        self.is_available = True

# Parent Class
class User:
    def __init__(self, user_id, name, max_books):
        self.user_id = user_id
        self.name = name
        self.max_books = max_books
        self.borrowed_books = {}

    def can_borrow(self):
        return len(self.borrowed_books) < self.max_books

    def borrow_book(self, book):
        if not self.can_borrow():
            print(f"{self.name} reached borrowing limit.")
            return False
        if not book.is_available:
            print("Book is not available.")
            return False
        book.borrow()
        self.borrowed_books[book.book_id] = date.today()
        return True

    def return_book(self, book_id):
        if book_id not in self.borrowed_books:
            print("Book not borrowed by this user.")
            return
        self.borrowed_books.pop(book_id)
        print(f"{self.name} returned the book successfully.")

# Teacher Class
class Teacher(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name, max_books=5)

# Student Class
class Student(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name, max_books=3)

# Library Class
class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Book '{book.title}' added successfully.")

    def register_user(self, user):
        self.users.append(user)
        print(f"User '{user.name}' registered successfully.")

    def find_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def find_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def borrow_book(self, user_id, book_id):
        user = self.find_user(user_id)
        book = self.find_book(book_id)
        if not user or not book:
            print("User or Book not found.")
            return
        if user.borrow_book(book):
            print(f"{user.name} borrowed '{book.title}' successfully.")

    def return_book(self, user_id, book_id):
        user = self.find_user(user_id)
        book = self.find_book(book_id)
        if not user or not book:
            print("User or Book not found.")
            return
        user.return_book(book_id)
        book.return_book()

    def show_all_books(self):
        print("\nAll Books:")
        for book in self.books:
            status = "Available" if book.is_available else "Borrowed"
            print(f"{book.book_id} - {book.title} by {book.author} ({status})")

    def show_all_users(self):
        print("\nAll Users:")
        for user in self.users:
            print(
                f"{user.user_id} - {user.name} "
                f"(Borrowed: {len(user.borrowed_books)}/{user.max_books})"
            )

library = Library()

# Add books
library.add_book(Book(1, "Clean Code", "Robert Martin"))
library.add_book(Book(2, "The Pragmatic Programmer", "Andrew Hunt"))
library.add_book(Book(3, "Design Patterns", "Erich Gamma"))

# Register users
library.register_user(Teacher(101, "Mr. Smith"))
library.register_user(Student(201, "Alice"))
library.register_user(Student(202, "Bob"))

# Borrow books
library.borrow_book(202, 3)
library.borrow_book(202, 1)
library.borrow_book(202, 2)


# Show all books and users
library.show_all_books()
library.show_all_users()

# Return books
library.return_book(202, 1)

# Show updated info
library.show_all_books()
library.show_all_users()
